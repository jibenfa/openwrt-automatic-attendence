# wifi-auto-duty
using bandwidthd and python scripts to record work attendance  on openwrt wifi router
利用bandwidthd和python脚本在openwrt无线路由上实现考勤功能（还可以记录每个mac的流量）。

前提：  
1.openwrt 路由安装了python包和bandwidthd  
2.登记每个接入wifi的设备的mac地址  


http(s)://路由ip/bandwidthd/qdb.html   查询考勤  
http(s)://路由ip/bandwidthd/ipname.html 查询流量排名  
