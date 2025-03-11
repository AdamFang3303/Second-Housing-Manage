from flask import Flask
from flask import render_template , request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# 配置数据库连接
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = '123456'
DATABASE = "flask_test"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

#初始化
db=SQLAlchemy(app)

# 定义数据库模型
class HouseInfo(db.Model):
    __tablename__ = 'house_info'
    id = db.Column(db.Integer, primary_key=True)
    house_info_link = db.Column(db.String(255), nullable=False)
    house_address = db.Column(db.String(255), nullable=False)
    house_type = db.Column(db.String(50), nullable=False)
    house_area = db.Column(db.Float, nullable=False)
    orientation = db.Column(db.String(50), nullable=False)
    decoration = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    house_category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    city = db.Column(db.String(50), nullable=False)

#测试数据库连接 在外面需要有应用上下文，在视图函数中 应用上下文已经包含在请求上下文中了，所以不需要
with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(text("Use sh_housing;"))
        rs=conn.execute(text("SHOW TABLES;"))
        print(rs.fetchone())

    
@app.route("/")
def index() :
    return render_template('index.html')


@app.route("/query" , methods=['GET','POST'])
def query() :
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name', '')
        street = request.form.get('street', '')
        min_price = request.form.get('min_price', None)
        max_price = request.form.get('max_price', None)
        min_area = request.form.get('min_area', None)
        max_area = request.form.get('max_area', None)
        decoration = request.form.get('decoration', '')
        building_type = request.form.get('building_type', '')
        min_year = request.form.get('min_year', None)
        max_year = request.form.get('max_year', None)
        direction = request.form.get('direction', '')

        # 构建查询
        query = HouseInfo.query

        if name:
            query = query.filter(HouseInfo.house_address.contains(name))
        if street:
            query = query.filter(HouseInfo.house_address.contains(street))
        if min_price:
            query = query.filter(HouseInfo.price >= min_price)
        if max_price:
            query = query.filter(HouseInfo.price <= max_price)
        if min_area:
            query = query.filter(HouseInfo.house_area >= min_area)
        if max_area:
            query = query.filter(HouseInfo.house_area <= max_area)
        if decoration:
            query = query.filter(HouseInfo.decoration == decoration)
        if building_type:
            query = query.filter(HouseInfo.house_type == building_type)
        if min_year:
            query = query.filter(HouseInfo.year >= min_year)
        if max_year:
            query = query.filter(HouseInfo.year <= max_year)
        if direction:
            query = query.filter(HouseInfo.orientation.contains(direction))

        houses = query.all()
    else:
        #展示全部的数据
        houses = HouseInfo.query.all()
    return render_template('data_query.html' , houses =houses)

@app.route("/heat_map")
def heat_map():
    return render_template('heat_map.html')


if __name__ == '__main__':
    app.run(debug=True)