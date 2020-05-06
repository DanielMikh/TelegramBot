class Admin():

    def list_to_str(self, _list):
        i = 1
        length = len(_list)
        text = 'Список разделов: '
        for section in _list:
            if i == length:
                text += str(section) + "."
            else:
                text += str(section) + ", "
            i += 1
        return text
