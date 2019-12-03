# coding:utf-8


class MyCache:

    def __init__(self):
        self.cache = {}

    def __contains__(self, key):
        return key in self.cache

    def get(self, key):
        return self.cache.get(key, '')

    @property
    def data(self):
        return self.cache

    def set(self, **kwargs):
        for k, v in kwargs.items():
            if k and v:
                self.cache[k] = v

    @property
    def size(self):
        return len(self.cache)


cache = MyCache()

if __name__ == '__main__':
    cache.set(a="aa", b='bb')
    print(cache.get("a"))
    print(cache.size)
    print(cache.data)
