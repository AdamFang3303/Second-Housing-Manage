项目基于https://github.com/BigLiuH/Second-hand-housing-information-query-and-prediction-system改变而来

1.前端交互界面使用HTML
2.后端使用Flask框架
3.数据与mysql数据库交互

data_manage : 存储了所有数据爬取，转换连接数据库，清洗相关操作的代码
data:原始数据
back_end: Flask框架代码和HTML templates等等
jupyter_test : 存储了绘图代码，使用pandas，numpy等库绘图

基本功能：
1.房价数据查询
2.小区数据查询
3.数据统计（可视化）
4.房价热力图

注：房价热力图调用百度API接口实现，出现数据无法加载情况可能需要用XAMPP打开Apache完成跨域请求