from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import func

app = Flask(__name__)

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 链接MySQL的用户名
USERNAME = "root"
# 链接mysql的密码
PASSWORD = "123456"
# MySQL上创建的数据库名称
DATABASE = "echarts"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

# 在app.config中设置好链接数据库的信息
# 使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中链接数据库的信息

db = SQLAlchemy(app)


# 学校名称 案件次数 累计金额
class UnivCount(db.Model):
    __tablename__ = "univcount"
    univName = db.Column(db.String(255), primary_key=True)
    count = db.Column(db.Integer)
    money = db.Column(db.Integer)


# 发生月份 月份诈骗金额
class MonthMoney(db.Model):
    __tablename__ = "monthmoney"
    month = db.Column(db.String(255), primary_key=True)
    money = db.Column(db.Integer)
    count = db.Column(db.Integer)


# 案件类型 发生次数 金额
class FraudWayCount(db.Model):
    __tablename__ = "fraudwaycount"
    fraudway = db.Column(db.String(255), primary_key=True)
    count = db.Column(db.Integer)
    money = db.Column(db.Integer)


# 按月份查询 案件类型 发生次数
class FraudData(db.Model):
    __tablename__ = '诈骗数据'
    id = db.Column(db.Integer, primary_key=True)
    fraudWay = db.Column(db.String(255))
    month = db.Column(db.String(255))


@app.route("/")
def query_datas():
    # 1.get查找:根据主键查找
    # user = User.query.get(1)
    # print(f"{user.id}:{user.username}-{user.password}")
    # 2.filter_by查找
    # Query:类数组
    # 学校名称 案件次数
    univName = []
    count = []

    data1 = UnivCount.query.order_by(UnivCount.count.desc()).all()
    data11 = UnivCount.query.order_by(UnivCount.money.desc()).limit(10).all()
    for data in data1:
        univName.append(data.univName)
        count.append(data.count)

    # 发生月份 月份诈骗金额
    month = []
    money = []
    count1 = []
    data2 = MonthMoney.query.all()
    for tdata in data2:
        month.append(tdata.month)
        money.append(tdata.money)
        count1.append(tdata.count)
    # 案件类型 发生次数
    fraudway = []
    tcount = []
    data3 = FraudWayCount.query.order_by(FraudWayCount.count.desc()).limit(5).all()

    for sdata in data3:
        fraudway.append(sdata.fraudway)
        tcount.append(sdata.count)
    df = pd.DataFrame({
        'name': fraudway,
        'value': tcount
    })
    dict1 = df.to_dict(orient="records")

    # 学校名称 发生次数 金额
    names = []
    schoolMoney = []
    sum = []
    for moneyData in data11:
        names.append(moneyData.univName)
        schoolMoney.append(moneyData.money)
        sum.append(moneyData.count)

    j = 0
    for i in schoolMoney:
        if i > j:
            j = i
    num = []
    for i in schoolMoney:
        x = (round(i / j, 2)) * 100
        num.append(x)

    # 案件类型 发生次数 金额 前十条
    fraudway2 = []
    moneycount = []
    fraudways = []
    data33 = FraudWayCount.query.order_by(FraudWayCount.money.desc()).limit(10).all()
    for wdata in data33:
        fraudway2.append(wdata.fraudway)
        moneycount.append(wdata.money)
        fraudways.append(wdata.fraudway)
    df = pd.DataFrame({
        'name': fraudway2,
        'value': moneycount
    })
    dict2 = df.to_dict(orient="records")

    # 案件类型 发生次数 金额 后十条
    fraudway3 = []
    moneycount2 = []
    data44 = FraudWayCount.query.order_by(FraudWayCount.money.asc()).limit(10).all()
    for qdata in data44:
        fraudway3.append(qdata.fraudway)
        moneycount2.append(qdata.money)
        fraudways.append(qdata.fraudway)
    df = pd.DataFrame({
        'name': fraudway3,
        'value': moneycount2
    })
    dict3 = df.to_dict(orient="records")


    # hide隐藏框
    # today = datetime.today()
    # newmonth = str(today.month)+"月"
    # hidefraud = []
    # hidecount = []
    # data5 = FraudData.query.filter_by(func.count(month=newmonth)).group_by(FraudData.fraudWay).all()
    # for hdata in data5:
    #     hidefraud.append(hdata.fraudWay)
    # print(hidefraud)







    return render_template("index.html",
                           count=count, univName=univName,
                           month=month, money=money, count1=count1,
                           dict1=dict1,
                           schoolMoney=schoolMoney, names=names, sum=sum, num=num,
                           dict2=dict2, dict3=dict3, fraudways=fraudways
                           )


if __name__ == '__main__':
    app.run()
