# BT-7274 discord bot

## commands

#### birthday
| command | Description |
| ----------- | ----------- |
| `/birthday set <day> <month>` | sets your birthday |
| `/birthday force_set <member> <day> <month>` | sets someone's birthday (authorized user only) |
| `/birthday get <user>` | gets someones birthday | 
| `/birthday next` | display a list of all the upcomming birthdays |

#### music

| command | Description |
| ----------- | ----------- |
| `/music play <query>` | plays or queue a music from a query |
| `/music skip` | skips to the next queued music (stops if None are next) |
| `/birthday stop` | stops the music and disconnects the bot | 
| `/birthday current` | display the current music playing along side a list of the upnext songs |

#### configuration

###### the commands bellow are authorized user only
| command | Description |
| ----------- | ----------- |
| `/config birthday_channel <optional:channel>` | set the server's default birthday annoucement channel (set to the system channel if None) |
| `/config authorize_role <role> <status>` | set someone's authorization status to true or false (admin only command) |

