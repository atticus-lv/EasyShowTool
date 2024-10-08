### v0.3.1

**修复**
替换默认NODE_PT_annotation面板的移除按钮以防止崩溃

### v0.3.0

**新功能**

+ 添加工具（将 添加 功能移动到新工具中）
    + 单击以选择活动
    + g/s/r 移动/缩放/旋转
    + 拖动以添加正方形/圆形
    + 拖动以添加带有刻度的新提示
    + 双击以添加具有原始大小的新提示
+ 调整工具（旧工具）
    + Shift + 单击以添加选择
    + Ctrl + 单击以删除选择

**修复**

+ 当没有 GP 数据时，拖动会报错

### v0.2.2

**修复**

+ 翻译
+ 选择清除问题

### v0.2.1

**新功能**

+ 改进多选功能
    + Shift + 单击以添加所选内容
    + Ctrl + 单击以删除所选内容
    + 选项：选择所有角/一个角以选择图层

**修复**

+ 无层时按 X 删除时出错

### v0.2.0

> 2024.8.3

**新功能**

+ 初步支持多选
    + 变换
        + 移动选中 g
        + 旋转选中 r
        + 缩放选中 s
    + 对齐与分布
        + 左/右/上/下对齐
        + 水平中心/垂直中心对齐
        + 水平分布/垂直分布
    + 颜色
        + 更改所选颜色
        + 更改选定的不透明度
        + 新用户界面
    + 删除
        + 删除所选对象

+ 缩放/旋转改进
    + 使用边界框中心而不是描边枢轴（在某些对象上效果不佳）

+ Blender svg 图标
    + 边界删除现在更准确

### v0.1.3

> 2024.7.17

**修复**

+ 在存在文件中未启用插件时确保内置字体
+ 新视图模式中的删除错误
+ 在后台模式下启用错误
+ 某些调试信息在发布模式下不会显示

**改变**

+ 视图绘制 不再需要点击显示，而是在切换到工具时及时显示
+ 现在插件可以作为扩展安装

### v0.1.2

> 2024.7.15

**修复**

+ 后台启用失败
+ 没有 3D 视图导入图标将不再报告错误
+ 没有上下文对象时的 alt 复制错误
+ 无活动层时的错误报告

### v0.1.1

> 2024.7.14

**新功能**

+ 添加对象
    + 添加属性厚度
    + 添加属性不透明度

+ 添加模态运算符 G 移动
    + 右键单击取消
    + 左键点击确认

+ 新的调色板系统（修复首次使用时的错误报告）
    + 提供预设颜色
    + 提供插座颜色
    + 使用弹出框面板显示

**修复**

+ 修复首次使用时的错误报告
+ Alt + 单击以复制移动将更改活动对象
+ 无3d视图导入图标时不再报错

### v0.1.0

> 2024.7.12

第一版