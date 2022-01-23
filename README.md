# GradeMapper

Программа для подсчёта среднего взвешенного оценок. Используются веса из Электронного журнала.

Протестировано на macOS(Intel), macOS(Apple Silicon)

Версия на [Swift](https://github.com/ivabus/GradeMapper-swift)

## Запуск

| Для macOS / Linux | Для Windows |
|-|-|
|1. Загружаем последний исходный код со страницы Releases | 1. Загружаем последний .zip архив для win64 со страницы Releases |
|2. Устанавливаем PyQt5 `pip3 install PyQt5` | 2. Запускаем `GradeMapper.exe` |
|3. Запускаем `GradeMapper.pyw` из архива с помощью `python3 GradeMapper.pyw` в папке с исходным кодом ||

### Устранение неполадок

Необходимы дополнительные действия для запуска на Apple Silicon:

    arch -x86_64 pip3 install PyQt5
    arch -x86_64 python3 GradeMapper.pyw


