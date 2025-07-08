import logging

import celery

from blog.models import Post


logger = logging.getLogger(__name__)

@celery.shared_task(
    bind=True,
    name="update_post_rating_new_user",
    max_retries=3,
    default_retry_delay=5,
)
def update_post_rating_new(self, post_id, rating):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNonExist:
        logger.warning(f"Post with id {post_id} does not exist")
        return

    try:
        post.rating = post.rating + rating
        post.ratings_count += 1
        post.save()
    except Exception as e:
        retries = self.request.retries
        logger.warning(f"Retry {retries} retries for post wit id {post_id} due to {e}")
        raise self.retry(exc=e)


@celery.shared_task(
    bind=True,
    name="update_post_rating_by_user_again",
    max_retries=3,
    default_retry_delay=5,
)
def update_post_rating_again(self, post_id, old_rating, rating):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNonExist:
        logger.warning(f"Post with id {post_id} does not exist")
        return

    try:
        post.rating = post.rating - old_rating + rating
        post.save()
    except Exception as e:
        retries = self.request.retries
        logger.warning(f"Retry {retries} retries for post wit id {post_id} due to {e}")
        raise self.retry(exc=e)
