ВЫВОД НАТИВНОЙ МОНЕТЫ И ERC20 ТОКЕНОВ С КОШЕЛЬКОВ

ШАГИ:
1) Скачать и установить Python: https://www.python.org/downloads
2) Активировать локальное окружение
    1. python -m venv venv
    2. Windows: venv\Scripts\activate.bat | Linux: source venv/bin/acitvate
3) Установить пакеты: pip install -r requirements.txt

ФАЙЛЫ:
1) multisender.py - перевод и нативной монеты, и токенов
2) eth_multisender.py - перевод нативной монеты
3) token_multisender.py - перевод токенов
4) private-keys.txt - приватные ключи
5) recipient-addresses.txt - адреса получателей
6) token-addresses.txt - адреса ERC20/BEP20 токенов
7) used-wallets.txt - использованные кошельки
8) config.json - файл с конфигом

CONFIG

| Поле             | Описание                                                                                             |
| -----------------|----------------------------------------------------------------------------------------------------- |
| rpc_url          | RPC Server Address - https://chainlist.org                                                           |
| unit             | единица измерения                                                                                    |
| gas_price        | цена за газовую единицу (если 0, то рассчитывается)                                                  |
| gas_limit        | лимит газа на транзакцию (если 0, то рассчитывается)                                                 |
| gas_limit_k      | коэффициент, на который умножается gas_limit                                                         |
| decimal_point    | дробная часть числа (число после запятой при рандомной генерации)                                    |
| max_amount       | true: перевод всех токенов с кошелька, false: перевод рандомного количества                          |
| max_value        | true: перевод всей нативной монеты с кошелька, false: перевод рандомного количества нативной монеты  |
| token_amount     | количество токенов: min - минимальное, max - максимальное                                            |
| token_amount     | количество нативной монеты: min - минимальное, max - максимальное                                    |
| delay            | время задержки между транзакциями                                                                    |
