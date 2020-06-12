import re

from instagram import WebAgent, Account

from dj_instaparser.models import InstagramAccount, Item

HASHTAG_MAX_LENGTH = 140


def validate_hashtag(hashtag):
    assert len(hashtag) <= HASHTAG_MAX_LENGTH, f'Hashtag #{hashtag} is too long.'
    assert re.match(r'^\w+$', hashtag), 'Hashtag shouldn\'t contain any special chars'


def _get_description_without_hashtags(description):
    description_words = description.split()
    words = [word for word in description_words if not word.startswith('#')]
    cleaned_description = ' '.join(words)
    return cleaned_description


def _get_item(post, remove_hashtags):
    if not post.is_album:
        images = [post.display_url]
    else:
        images = [image.display_url for image in post.album]

    description = post.caption or ''
    item = {
        'description': _get_description_without_hashtags(description) if remove_hashtags else description,
        'images': images
    }
    return item


def get_store_items(store_id, sale_hashtag, remove_hashtags=True):
    agent = WebAgent()
    account = Account(store_id)
    agent.update(account)

    assert not account.is_private, 'Account is private!'

    new_acc, created = InstagramAccount.objects.get_or_create(name=store_id)
    if not created:
        old_items = Item.objects.filter(account=new_acc)
        old_items.delete()

    media, pointer = agent.get_media(account, count=account.media_count)
    items = []
    for post in media:
        description = post.caption or ''
        if sale_hashtag:
            # post_contain_hashtag = any([hashtag in description for hashtag in sale_hashtags])
            post_contain_hashtag = sale_hashtag in description
            if not post_contain_hashtag:
                continue
        items.append(_get_item(post, remove_hashtags))

    for item in items:
        if item.get('images'):
            Item.objects.create(account=new_acc, description=item.get('description'), image_url=item.get('images')[0])
    return items

