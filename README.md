# GradeMapper

Программа для подсчёта среднего взвешенного оценок. Используются веса из Электронного журнала.

Протестировано на macOS (Intel), macOS (Apple Silicon), Arch Linux

Версия на [Swift](https://github.com/ivabus/GradeMapper-swift)

## Запуск

| Для macOS / Linux / Windows |
|-|
| 1. Загружаем последний исходный код в .zip с главной страницы |
| 2. Распаковываем архив |
| 3. Устанавливаем PyQt5 `pip3 install PyQt5` |
| 4. В папке с исходным кодом запускаем `GradeMapper.pyw` с помощью `python3 GradeMapper.pyw` |

(Раньше на странице Releases был .exe-файл, но после удаления репозитория он пропал. Собирать его заново мне лень, так что запускайте программу из сырцов.)

### Устранение неполадок

На macOS необходимо установить Xcode или Xcode CLT, что можно сделать с помощью

    xcode-select --install

Необходимы дополнительные действия для запуска на Apple Silicon:

    softwareupdate --install-rosetta
    arch -x86_64 pip3 install PyQt5
    arch -x86_64 python3 GradeMapper.pyw

