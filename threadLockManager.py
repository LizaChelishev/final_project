from threading import Lock, Event


class ThreadLockManager:
    _instance = None
    _lock = Lock()
    _locks_dict_lock = Lock()
    _answers_from_core_lock = Lock()

    def __init__(self):
        self.locks_dict = {}
        self.answers_from_core_dict = {}
        raise RuntimeError('Call get_instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)

                cls._instance.locks_dict = {}  # request_id[str]: Lock
                cls._instance.answers_from_core_dict = {}  # request_id[str]: answer_from_core[dict]

                return cls._instance
            else:
                return cls._instance

    def lock_thread(self, request_id: str):
        e = Event()  # creating a Lock instance
        with self._locks_dict_lock:
            self.locks_dict[request_id] = e  # mapping in with the request id into the dict
        print('locks_dict', self.locks_dict)
        e.wait()  # locking with thread

    def handle_answer_release_thread(self, request_id: str, data: dict):
        with self._answers_from_core_lock:
            self.answers_from_core_dict[request_id] = data
        with self._locks_dict_lock:
            e = self.locks_dict.pop(request_id)
        e.set()

    def get_answer(self, request_id: str):
        print('trying to get answer')
        print(self.answers_from_core_dict)
        with self._answers_from_core_lock:
            return self.answers_from_core_dict.pop(request_id)
