# openwrt-automatic-attendence
using bandwidthd and python scripts to record work attendance and network flow on openwrt wifi router

利用bandwidthd和python脚本在openwrt无线路由上实现wifi自动考勤功能（还可以记录每个mac的流量），还可以通过路由自动发考勤至指定邮箱。

前提：  
1.openwrt 路由安装了python包和bandwidthd  
2.登记每个接入wifi的设备的mac地址，默认放在/root/maclist.txt


http(s)://路由ip/bandwidthd/qdb.html   查询考勤  
http(s)://路由ip/bandwidthd/ipname.html 查询流量排名  
