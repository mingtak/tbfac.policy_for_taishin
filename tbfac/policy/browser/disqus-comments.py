from Products.Five.browser import BrowserView
from ..util import getLatestComments


class RecentCommentsView(BrowserView):

    def getComments(self):
        """Returns list of latest comments"""
        comments = []
        posts, threads = getLatestComments(self.context)
        for cc in posts:
            thread_id = cc.get('thread', '')
            thread = {}
            if thread_id and thread_id in threads:
                thread = {
                    'title': threads[thread_id].get('title', 'No Title'),
                    'url': threads[thread_id].get('link', ''),
                }
            body = cc.get('raw_message', '')
            if len(body) > 30:
                body = body[:30] + '...'
#            import pdb; pdb.set_trace()
            if not thread.get('url', ''):
                continue
            comments.append({
                'author': cc.get('author', {}).get('name', 'Anonymous'),
                'date': cc.get('createdAt', ''),
                'body': body,
                'thread': thread,
                'url': '%s#comment-%s' % (thread.get('url', ''), cc.get('id',
                    '')),
            })
        return comments

