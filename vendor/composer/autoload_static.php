<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInitf74b2a19b15c095f598d0f60a1f5fdba
{
    public static $prefixLengthsPsr4 = array (
        'M' => 
        array (
            'Mike42\\' => 7,
        ),
    );

    public static $prefixDirsPsr4 = array (
        'Mike42\\' => 
        array (
            0 => __DIR__ . '/..' . '/mike42/escpos-php/src/Mike42',
        ),
    );

    public static $classMap = array (
        'Composer\\InstalledVersions' => __DIR__ . '/..' . '/composer/InstalledVersions.php',
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixLengthsPsr4 = ComposerStaticInitf74b2a19b15c095f598d0f60a1f5fdba::$prefixLengthsPsr4;
            $loader->prefixDirsPsr4 = ComposerStaticInitf74b2a19b15c095f598d0f60a1f5fdba::$prefixDirsPsr4;
            $loader->classMap = ComposerStaticInitf74b2a19b15c095f598d0f60a1f5fdba::$classMap;

        }, null, ClassLoader::class);
    }
}
