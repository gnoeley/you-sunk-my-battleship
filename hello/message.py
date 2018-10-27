class Message:

    def __init__(self, msg_id, from_num, to_num, keyword, content):
        self.msgId = msg_id
        self.fromNum = from_num
        self.toNum = to_num
        self.keyword = keyword
        self.content = content


    def __str__(self):
        return \
            "Message: {" + "msgId:" + self.msgId + ", " + "fromNum:" + self.fromNum + ", " + "toNum:" + self.toNum + ", keyword:" + self.keyword + ", " +"content:" + self.content + "}"

