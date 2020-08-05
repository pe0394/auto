from locust import HttpUser, TaskSet, task, between,SequentialTaskSet
import csv
import json
import queue    #导入队列
from locust.contrib.fasthttp import FastHttpUser    #异步请求,不考虑服务端返回的数据

class MySeqTasks(SequentialTaskSet):
#class MyTaskSet(TaskSet):
    logindata = queue.Queue()   #队列实例化
    csvFile = open(r'D:\\Auto\\test\\username1.csv', 'r')   #读取本地csv，只读模式
    reader = csv.reader(csvFile)
    for row in reader:      #循环遍历将表内账号密码放入logindata
        logindata.put({"account": row[0], "password": row[1], "page": "0"})
    logindata.task_done()   #
    #print('--------------------------------on_start---------------------------------')
    #如果要登录接口只跑一次，需要注销掉这个task任务和def LoginAccountJson方法,要循环跑登录，就要注销掉on_start
    # @task
    # def LoginAccountJson(self):
    def on_start(self):
        data = self.logindata.get()     #获取队列里的数据
        url = '/AccountService.asmx/LoginAccountJson'
        headers = {'Host': 'test.ws.forclass.net'}
        try:
            data
        except queue.Empty:     #队列取空后，直接退出
            exit(0)
        with self.client.post(url, headers=headers, data=data, catch_response=True, name='登录') as response:
            if response.status_code == 200 and response.json()['ReturnCode'] == 1:  # 断言状态码status_code等于200，再断言response.json的返回结果中，ReturnCode等于1
                response.success()
                print('登录成功', response.text)
                self.session = (response.json()["result"][0]["session"])  # 获取response.json返回结果中的session值，由于result后是数组，获取数组定位要加[0]
                # print(self.session)        #打印response.json返回结果中的session值
            else:
                print(response.text, '登录失败')
                response.failure('LoginAccountJson_ 接口失败！')
        return self.session

    @task
    def GetSCStudentAssignmentList(self):
        url = '/ANAService.asmx/GetSCStudentAssignmentList'
        data = {"session": self.session,
                "page": "1",
                "count": "7",
                "index": "1",
                "stateName": "",
                "subject":"",
                "sName":"批阅完成",
                "fromDate":"2020-06-06","toDate":"2020-07-07"
                }
        headers = {
            'Host': 'test.zzn.forclass.net',
            'Content-Type': 'application/json; charset=utf-8'
        }
        with self.client.post(url,  data=data, catch_response=True, name='获取学生作业列表')as response:
            #print(response.text)

            if response.status_code == 200 and '<ReturnCode>1</ReturnCode>' in response.text:
                response.success()
            else:
                print(response.text, '获取学生作业列表失败')
                response.failure('GetSCStudentAssignmentList_ 接口失败！')


    @task
    def UploadAssignmentAnswer_New(self):
        url = '/ANAService.asmx/UploadAssignmentAnswer_New'
        false = False
        true = True
        jsondata = {"session":self.session,"task_id":28616,"score":0,"duration":231,"is_single":false,"is_done":false,"answer_list":[{"Idx":"210932","Answer":"","Duration":"15","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"210933","Answer":"","Duration":"15","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"210961","Answer":"","Duration":"7","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"210962","Answer":"","Duration":"7","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"210963","Answer":"","Duration":"7","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"210964","Answer":"","Duration":"7","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"210965","Answer":"","Duration":"7","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"210999","Answer":"","Duration":"9","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"211069","Answer":"<div class=\"umanswer\"><div class=\"umpreset\"><img class=\"umpreanswer\" src=\"http://fcdata.forclass.net/QaRes/63552000/63552000-5292271721349.png\" width=\"592\" height=\"122\"></div><div class=\"umuseranswer\" style=\"top: -122px; height: 197px;\" width=\"625\" height=\"460\"><img class=\"umuseranswerimg\" crossorigin=\"anonymous\" src=\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_28616_qo211069.png?t=1594188498433\" w=\"625\" h=\"460\"></div></div>","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619188","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619189","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619190","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619233","Answer":"","Duration":"26","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619234","Answer":"","Duration":"26","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619235","Answer":"","Duration":"26","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619271","Answer":"","Duration":"18","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619272","Answer":"","Duration":"18","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619273","Answer":"","Duration":"18","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619274","Answer":"","Duration":"18","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619275","Answer":"","Duration":"18","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619276","Answer":"","Duration":"18","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619282","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619283","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619284","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619285","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619286","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619287","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619288","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619289","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619290","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619291","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619332","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619333","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619334","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619335","Answer":"<div class=\"umanswer\"><div class=\"umpreset\"><img class=\"umpreanswer\" src=\"http://fcdata.forclass.net/QaRes/63570000/63570000-2363673827934.png\" width=\"558\" height=\"303\"></div><div class=\"umuseranswer\" style=\"top: -303px; height: 16px;\" width=\"720\" height=\"462\"><img class=\"umuseranswerimg\" crossorigin=\"anonymous\" src=\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_28616_qo3619335.png?t=1594188551945\" w=\"720\" h=\"462\"></div></div>","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619338","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619339","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619340","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619366","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619367","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619368","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619369","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619370","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619371","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619389","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619390","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716812","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716813","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716814","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716880","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716881","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716882","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716883","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716884","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716885","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716886","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716887","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716888","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716889","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716890","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716919","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716920","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716921","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716922","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716923","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716947","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3716948","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3717072","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3717073","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3717074","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3717089","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3717090","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3717121","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3717122","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3818516","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3818517","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3818518","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3824057","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3830686","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3830687","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3830688","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3830718","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3830719","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3830720","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3830721","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858357","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858358","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858359","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858360","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858361","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858362","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858363","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858364","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858365","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858366","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858367","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858368","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858369","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858370","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858371","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858372","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858373","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858374","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858375","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858376","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858377","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858378","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858379","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858380","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858381","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858382","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858383","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858384","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858385","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858386","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858387","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858388","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858389","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858390","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858391","Answer":"","Duration":"4","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858392","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858393","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858394","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858395","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3858396","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3859594","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3859595","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3859596","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3859597","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3859598","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3859599","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3859600","Answer":"","Duration":"3","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3880289","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3880290","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3880291","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3880292","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3880293","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3880294","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3880295","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869198","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869199","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869200","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869201","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869281","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869282","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869283","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3869284","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3947447","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3947448","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3947449","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3947450","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3947451","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3947452","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3947453","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619266","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619267","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619268","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619269","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619270","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619323","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619324","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619325","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619326","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619327","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619356","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619357","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619358","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619359","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619372","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619373","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619374","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619375","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619376","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619377","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619378","Answer":"","Duration":"7","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619379","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619380","Answer":"","Duration":"1","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619381","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619424","Answer":"","Duration":"2","IsCloze":true,"IsCorrect":false,"IsImage":false},{"Idx":"3619425","Answer":"","Duration":"6","IsCloze":true,"IsCorrect":false,"IsImage":false}],"img_json":"[{\"question_id\":\"34776\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188479540.png?t=1594188479845\"]},{\"question_id\":\"34790\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188486058.png?t=1594188486310\"]},{\"question_id\":\"34805\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188495500.png?t=1594188495701\"]},{\"question_id\":\"34852\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_28616_qo211069.png?t=1594188498433\"]},{\"question_id\":\"192685\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188499948.png?t=1594188500177\"]},{\"question_id\":\"192717\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188526759.png?t=1594188526945\"]},{\"question_id\":\"192743\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188543484.png?t=1594188543644\"]},{\"question_id\":\"192749\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188545134.png?t=1594188545292\"]},{\"question_id\":\"192750\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188546944.png?t=1594188547105\"]},{\"question_id\":\"192751\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188548547.png?t=1594188548736\"]},{\"question_id\":\"192782\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188550247.png?t=1594188550399\"]},{\"question_id\":\"192783\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_28616_qo3619335.png?t=1594188551945\"]},{\"question_id\":\"192786\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188553414.png?t=1594188553611\"]},{\"question_id\":\"192806\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188554760.png?t=1594188555067\"]},{\"question_id\":\"192807\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188556407.png?t=1594188556563\"]},{\"question_id\":\"192808\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188558016.png?t=1594188558335\"]},{\"question_id\":\"192825\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188559377.png?t=1594188559559\"]},{\"question_id\":\"264649\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188560879.png?t=1594188561060\"]},{\"question_id\":\"264683\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188562325.png?t=1594188562479\"]},{\"question_id\":\"264684\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188563745.png?t=1594188563897\"]},{\"question_id\":\"264701\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188565205.png?t=1594188565357\"]},{\"question_id\":\"264722\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188566677.png?t=1594188566833\"]},{\"question_id\":\"264796\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188568138.png?t=1594188568296\"]},{\"question_id\":\"264804\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188569682.png?t=1594188569845\"]},{\"question_id\":\"264820\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188571093.png?t=1594188571255\"]},{\"question_id\":\"1147545\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188572610.png?t=1594188572895\"]},{\"question_id\":\"1148701\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188574106.png?t=1594188574263\"]},{\"question_id\":\"1151109\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188575689.png?t=1594188575978\"]},{\"question_id\":\"1151110\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188577178.png?t=1594188577329\"]},{\"question_id\":\"1151111\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188578638.png?t=1594188578795\"]},{\"question_id\":\"1151164\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188580153.png?t=1594188580449\"]},{\"question_id\":\"1151165\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188581510.png?t=1594188581663\"]},{\"question_id\":\"1151166\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188582905.png?t=1594188583062\"]},{\"question_id\":\"1159971\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188584240.png?t=1594188584396\"]},{\"question_id\":\"1159972\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188585711.png?t=1594188585872\"]},{\"question_id\":\"1159973\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188586963.png?t=1594188587116\"]},{\"question_id\":\"1159974\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188588348.png?t=1594188588494\"]},{\"question_id\":\"1159975\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188589834.png?t=1594188589986\"]},{\"question_id\":\"1159976\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188591261.png?t=1594188591429\"]},{\"question_id\":\"1159977\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188592648.png?t=1594188592849\"]},{\"question_id\":\"1159978\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188594111.png?t=1594188594429\"]},{\"question_id\":\"1159979\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188595572.png?t=1594188595724\"]},{\"question_id\":\"1159980\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188597043.png?t=1594188597194\"]},{\"question_id\":\"1159981\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188598481.png?t=1594188598634\"]},{\"question_id\":\"1159982\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188599830.png?t=1594188599979\"]},{\"question_id\":\"1159983\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188601183.png?t=1594188601380\"]},{\"question_id\":\"1159984\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188602853.png?t=1594188603007\"]},{\"question_id\":\"1159985\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188604137.png?t=1594188604330\"]},{\"question_id\":\"1159986\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188605562.png?t=1594188605713\"]},{\"question_id\":\"1159987\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188606961.png?t=1594188607112\"]},{\"question_id\":\"1159988\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188608314.png?t=1594188608464\"]},{\"question_id\":\"1159989\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188609615.png?t=1594188609784\"]},{\"question_id\":\"1159990\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188610963.png?t=1594188611111\"]},{\"question_id\":\"1159991\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188612212.png?t=1594188612365\"]},{\"question_id\":\"1159992\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188613580.png?t=1594188613740\"]},{\"question_id\":\"1159993\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188615036.png?t=1594188615199\"]},{\"question_id\":\"1159994\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188616319.png?t=1594188616534\"]},{\"question_id\":\"1159995\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188617690.png?t=1594188617847\"]},{\"question_id\":\"1159996\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188618853.png?t=1594188619015\"]},{\"question_id\":\"1159997\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188620172.png?t=1594188620330\"]},{\"question_id\":\"1159998\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188621511.png?t=1594188621668\"]},{\"question_id\":\"1159999\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188623473.png?t=1594188623692\"]},{\"question_id\":\"1160000\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188624862.png?t=1594188625024\"]},{\"question_id\":\"1160001\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188626144.png?t=1594188626354\"]},{\"question_id\":\"1160002\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188627501.png?t=1594188627658\"]},{\"question_id\":\"1160003\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188628835.png?t=1594188629043\"]},{\"question_id\":\"1160004\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188630192.png?t=1594188630345\"]},{\"question_id\":\"1160005\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188634303.png?t=1594188634463\"]},{\"question_id\":\"1160006\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188635781.png?t=1594188635929\"]},{\"question_id\":\"1160007\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188637122.png?t=1594188637280\"]},{\"question_id\":\"1160008\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188638570.png?t=1594188638728\"]},{\"question_id\":\"1160009\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188639918.png?t=1594188640087\"]},{\"question_id\":\"1160010\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188641367.png?t=1594188641529\"]},{\"question_id\":\"1160291\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188644579.png?t=1594188644796\"]},{\"question_id\":\"1160292\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188646082.png?t=1594188646229\"]},{\"question_id\":\"1160784\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188647818.png?t=1594188648011\"]},{\"question_id\":\"1160785\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188649153.png?t=1594188649314\"]},{\"question_id\":\"1162095\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188650588.png?t=1594188650746\"]},{\"question_id\":\"1162116\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188651988.png?t=1594188652145\"]},{\"question_id\":\"1185679\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188653317.png?t=1594188653485\"]},{\"question_id\":\"1185680\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188654755.png?t=1594188654951\"]},{\"question_id\":\"192741\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188656025.png?t=1594188656179\"]},{\"question_id\":\"192742\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188658236.png?t=1594188658395\"]},{\"question_id\":\"192776\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188659911.png?t=1594188660107\"]},{\"question_id\":\"192777\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188661477.png?t=1594188661632\"]},{\"question_id\":\"192796\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188663036.png?t=1594188663242\"]},{\"question_id\":\"192797\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188664545.png?t=1594188664742\"]},{\"question_id\":\"192798\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188666194.png?t=1594188666345\"]},{\"question_id\":\"192799\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188667765.png?t=1594188667928\"]},{\"question_id\":\"192809\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188669402.png?t=1594188669562\"]},{\"question_id\":\"192810\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188671023.png?t=1594188671180\"]},{\"question_id\":\"192811\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188672733.png?t=1594188672879\"]},{\"question_id\":\"192812\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188674256.png?t=1594188674413\"]},{\"question_id\":\"192813\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188675811.png?t=1594188676017\"]},{\"question_id\":\"192814\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188677413.png?t=1594188677584\"]},{\"question_id\":\"192815\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188678914.png?t=1594188679062\"]},{\"question_id\":\"192816\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188680585.png?t=1594188680874\"]},{\"question_id\":\"192817\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188682139.png?t=1594188682309\"]},{\"question_id\":\"192818\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188683601.png?t=1594188683881\"]},{\"question_id\":\"192841\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188686919.png?t=1594188687213\"]},{\"question_id\":\"192842\",\"img_list\":[\"http://forcass-res.oss-cn-qingdao.aliyuncs.com/AttachFiles/3010499/2020_07_08_3010499_qo1594188688972.png?t=1594188689148\"]}]","question_askes_json":"[]","audio_json":"[]","page":0}
        headers = {'Content-Type': 'application/json'}
        jsonstr = json.dumps(jsondata)  #将json数据转换成字符串
        with self.client.post(url, data=jsonstr, headers=headers, catch_response=True, name='学生提交作业')as response:
            #print(response.text)
            if response.status_code == 200 and '"ReturnCode":1' in response.text:
                #print('提交作业成功')
                response.success()
            else:
                print(response.text, '提交作业失败')
                response.failure('UploadAssignmentAnswer_New_ 接口失败！')
            #print(jsondata)



class WebsiteUser(FastHttpUser):
    host = 'http://test.zzn.forclass.net'
    tasks = [MySeqTasks]
    wait_time = between(0.1, 0.2)   # 设置请求的思考时间范围,单位是秒


if __name__ == '__main__':
    import os

    # 启动脚本，以最大请求200个，每秒步进为20
    os.system('locust -f locust_paas.py --headless -u 200 -r 20')
