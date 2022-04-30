# Skanestas Test Task
Displaying fake financial data

----
## Requirements

### Dependencies

* Docker 19.03.6+
* Compose 2.2.3+
### Network
Ports 80, 6379, 8086 should not be bound to any other process on the target machine

## Launch

To get started with all the defaults, simply clone the repo:
```bash
git clone https://github.com/Strady/skanestas.git
```
Go to the project directory:
```bash
cd skanestas
```
And execute:
```bash
docker-compose up -V
```
It takes about 1 minute for all internal services to start. To see a plot with financial open the [localhost page](http://127.0.0.1) in a browser.