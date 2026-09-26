function gnomeSort(array) {
    var position = 1;

    while (position < array.length) {
        if (position === 0 || array[position - 1] <= array[position]) {
            position = position + 1;
        } else {
            var temporary = array[position];
            array[position] = array[position - 1];
            array[position - 1] = temporary;

            position = position - 1;
        }
    }

    return array;
}


function sortArray() {
    var text = document.getElementById("arrayInput").value;

    text = text.trim();

    // Проверяем, что строка не пустая.
    if (text === "") {
        document.getElementById("result").innerHTML =
            "Ошибка: введите хотя бы одно число.";
        return;
    }

    var parts = text.split(" ");
    var numbers = [];

    // Превращаем каждую часть строки в число.
    for (var i = 0; i < parts.length; i++) {
        // Несколько пробелов подряд пропускаем.
        if (parts[i] !== "") {
            var number = Number(parts[i]);

            if (isNaN(number)) {
                document.getElementById("result").innerHTML =
                    "Ошибка: массив должен содержать только числа через пробел.";
                return;
            }

            numbers.push(number);
        }
    }

    var sortedNumbers = gnomeSort(numbers);

    // Выводим отсортированный массив на страницу.
    document.getElementById("result").innerHTML =
        "Отсортированный массив: " + sortedNumbers.join(" ");
}
