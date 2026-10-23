---
type: tool
category: linux
tags:
  - scripting-language
  - programming-language
---
# Overview

## Quick Commands
### Downloading File using Ruby
```ruby
ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh")))'
```