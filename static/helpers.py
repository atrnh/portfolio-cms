"""Helpers for use with model.py"""


from datetime import datetime
import json
from collections import deque


class JSONMixin(object):
    """JSON helper mixins."""

    @staticmethod
    def get_json_from_list(instances):
        """Return JSON of a list of instances."""

        return json.dumps(
            [json.loads(instance.get_attributes()) for instance in instances]
        )

    def get_attributes(self):
        """Get the attributes of an instance and their values.

        Does not include private attributes.
        """

        attributes = {}

        for attribute, value in self.__dict__.iteritems():
            if not attribute.startswith('_'):
                if type(value) is datetime:
                    attributes[attribute] = value.isoformat()
                elif isinstance(value, list):
                    try:
                        # We want a Python list instead of a JSON string since
                        # it will already get converted to JSON in
                        # return statement
                        attributes[attribute] = json.loads(
                            self.get_json_from_list(value)
                        )
                    except IndexError:
                        attributes[attribute] = []
                elif isinstance(value, db.Model):
                    attributes[attribute] = json.loads(value.get_attributes())
                else:
                    attributes[attribute] = value

        return json.dumps(attributes)


class DeleteHistory(object):
    """Keep track of deletions to allow undoing them."""

    def __init__(self, maxlen):
        """Create a DeleteHistory.

        DeleteHistory is implemented with a deque. Up to maxlen deleted items
        are stored in the deque. Old items will be deleted from the database
        permanently to make room for new items.
        """

        self._history = deque(maxlen=maxlen)

    def __repr__(self):
        """Console representation of DeleteHistory."""

        return '<DeleteHistory maxlen={maxlen} len={len}>'.format(
            maxlen=self._history.maxlen,
            len=len(self._history),
        )

    def queue(self, obj):
        """Queue an object for deletion."""

        # Delete oldest item if deque is full
        if len(self._history) == self._history.maxlen:
            db.session.delete(self._history.popleft())
            db.session.commit()

        self._history.append(obj)

    def pop(self):
        """Pop an object to undo."""

        return self._history.pop()
