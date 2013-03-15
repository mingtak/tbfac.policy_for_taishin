from Products.Five.browser import BrowserView
from ..util import getLatestComments


class RecentCommentsView(BrowserView):

    def getComments(self):
        """Returns list of latest comments"""
        comments = []
        posts, threads = getLatestComments(self.context)
        for c in posts:
            thread_id = c.get('thread', '')
            thread = {}
            if thread_id and thread_id in threads:
                thread = {
                    'title': threads[thread_id].get('title', 'No Title'),
                    'url': threads[thread_id].get('link', ''),
                }
            body = c.get('raw_message', '')
            if len(body) > 30:
                body = body[:30] + '...'
            comments.append({
                'author': c.get('author', {}).get('name', 'Anonymous'),
                'body': body,
                'thread': thread,
                'url': '%s#comment-%s' % (thread.get('url', ''), c.get('id',
                    '')),
            })
        return comments

