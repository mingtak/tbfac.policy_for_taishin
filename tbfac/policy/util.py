from time import time
from disqusapi import Paginator

from plone.memoize.ram import cache

from .config import LATEST_COMMENTS_LIMIT, DISQUS_API_CALL_TIMEOUT
from .api import DisqusAPI


def _cache_key(fun, *args, **kw):
    timeout = time() // DISQUS_API_CALL_TIMEOUT
    if args:
        return (timeout, args[0])
    else:
        return (timeout,)

class DisqusEmptyResponseError(Exception):
    __doc__ = u"Empty response from DISQUS API call."

@cache(_cache_key)
def _disqusLatestsPosts(context, limit=LATEST_COMMENTS_LIMIT):
    """Returns all threads mapping by uid"""
    disqus = DisqusAPI(context)
    posts = []
    thread_ids = []

    # collect list of latest 'limit' posts
    try:
        for post in Paginator(disqus.posts.list, limit=limit):
            posts.append(post)
            thread_id = post.get('thread', '')
            if thread_id and thread_id not in thread_ids:
                thread_ids.append(thread_id)
    except Exception:
        pass
    else:
        # raise here exception for not cache empty response
        if not posts:
            raise DisqusEmptyResponseError()

    # collect required threads
    threads = {}
    if thread_ids:
        try:
            for thread in Paginator(disqus.threads.list, thread=thread_ids):
                threads[thread.get('id', '')] = thread
        except Exception:
            pass

    return posts, threads

def getLatestComments(context):
    try:
        posts, threads = _disqusLatestsPosts(context)
    except DisqusEmptyResponseError:
        return [], {}
    else:
        return posts, threads

@cache(_cache_key)
def _disqusLatestsPostsByThreads(context, threads, limit=LATEST_COMMENTS_LIMIT):
    """Returns all threads mapping by uid.

    @threads - list of thread ids to get
    """
    disqus = DisqusAPI(context)
    posts = []

    # collect list of latest 'limit' posts
    try:
        for post in Paginator(disqus.posts.list, thread=threads, limit=limit):
            posts.append(post)
    except Exception:
        pass
    else:
        # raise here exception for not cache empty response
        if not posts:
            raise DisqusEmptyResponseError()

    return posts

def getLatestCommentsByThreads(context, threads, limit=LATEST_COMMENTS_LIMIT):
    try:
        posts = _disqusLatestsPostsByThreads(context, threads, limit=limit)
    except DisqusEmptyResponseError:
        return [], {}
    else:
        return posts

@cache(_cache_key)
def _disqusThreads(context):
    """Returns all threads mapping by uid.

    @threads - list of thread ids to get
    """
    disqus = DisqusAPI(context)
    threads = {}

    try:
        for thread in Paginator(disqus.threads.list, limit=100):
            for thread_uid in thread['identifiers']:
                threads[thread_uid] = thread
    except Exception:
        pass

    # raise here exception for not cache empty response
    if not threads:
        raise DisqusEmptyResponseError()

    return threads

def getDisqusThreads(context):
    try:
        threads = _disqusThreads(context)
    except DisqusEmptyResponseError:
        return {}
    else:
        return threads
