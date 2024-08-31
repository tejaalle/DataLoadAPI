class Globals():
    dic = None
    def init(self):
        self.dic = {}
    def set(self, key, value):
        if value is None:
            return False
        self.dic[key] = value
        return True
    def get(self, key):
        return self.dic.get(key, None)


globals =Globals()