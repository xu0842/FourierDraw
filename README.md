# 傅里叶变换绘图-网页版-v3
--------------------------------------
- 版本: 2022年4月第三版
- 在线网页: <https://www.xcreate.cool/test/imgtest/imgDraw.html>
- 演示视频: [BV1cY411u7jU](https://www.bilibili.com/video/BV1cY411u7jU?spm_id_from=333.999.0.0&vd_source=09a1b1eba90b464c2c46c4c894480343)

<img src="./img/example.png" width="60%">

### 1、文件结构

- `front-end` 前端代码
- `py-back-end`后端python代码
- `img` 一些测试过程的图片

### 2、测试方法

- 安装好python依赖后，运行`py-back-end`中的`server.py`,之后浏览器打开`imgDraw.html`即可。
  
### 3、功能

- 加载图片后经过一系列分析即可绘图
- 支持降采样重绘

### 4、分析流程


$$\begin{CD}
  原图 @>canny边缘提取>> 边缘二值图 @> 带惯性的深度优先搜索 >> 连通路径序列 @> 蚁群优化处理 >> 尽量短的欧拉回路 @> 一维离散傅里叶变换 >> 用于绘图的频谱序列
\end{CD}$$


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
