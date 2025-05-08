// ajax-запрос структуры типов, категорий, подкатегорий, статусов
async function getStructureData() {
  try {
    const response = await fetch('/api/structure-data/');
    if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Не удалось загрузить данные:', error);
    return null;
  }
}

// Вспомогательная функция для заполнения select
function fillSelect(selectElement, items) {
    selectElement.innerHTML = ''; // Очищаем список
  
    // Добавляем первые пустые option
    if (selectElement.id === 'typeflow') {
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Выберите тип';
        selectElement.appendChild(defaultOption);
    }
    if (selectElement.id === 'category') {
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Выберите категорию';
        selectElement.appendChild(defaultOption);
    }
    if (selectElement.id === 'subcategory') {
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Выберите подкатегорию';
        selectElement.appendChild(defaultOption);
    }
  
    // Заполняем options
    for (const [id, name] of Object.entries(items)) {
        const option = document.createElement('option');
        option.value = id;
        option.textContent = name;
        selectElement.appendChild(option);
    }
}

// // Вспомогательная функция для заполнения выпадающих списков
// function fillSelect(selectElement, options) {
//     options.forEach(option => {
//         const opt = document.createElement('option');
//         opt.value = option;
//         opt.textContent = option;
//         selectElement.appendChild(opt);
//     });
// }


// // ======= Заполнение выпадающих списков  =======
// async function fillDropdownLists() {
//     filterData = await getStructureData();
//     
//     // Элементы формы
//     const typeflowSelect = document.getElementById('typeflow');
//     const categorySelect = document.getElementById('category');
//     const subcategorySelect = document.getElementById('subcategory');
//     const statusSelect = document.getElementById('status');
//
//     // Заполняем статичные поля
//     fillSelect(typeflowSelect, filterData.typeflows);
//     fillSelect(statusSelect, filterData.statuses);
//
//     // Если форма редактирования и есть выбранный тип
//     if (typeflowSelect.value && document.getElementById('form-update-flow')) {
//         updateCategories(typeflowSelect.value, true);
//     }
//
//     // Обработчик изменения типа
//     typeflowSelect.addEventListener('change', function() {
//         updateCategories(this.value);
//     });
//
//     // Если форма редактирования и есть выбранная категория
//     if (categorySelect.value && document.getElementById('form-update-flow')) {
//         updateSubcategories(categorySelect.value, true);
//     }
//
//     // Обработчик изменения категории
//     categorySelect.addEventListener('change', function() {
//         updateSubcategories(this.value);
//     });
// }
//

// // Вынесем обновление категорий в отдельную функцию
// function updateCategories(selectedType, isInitialLoad = false) {
//     const categorySelect = document.getElementById('category');
//     const subcategorySelect = document.getElementById('subcategory');
//     
//     // Сохраняем текущее значение перед обновлением
//     const currentCategory = isInitialLoad ? categorySelect.value : null;
//     
//     // Сбрасываем подкатегории
//     subcategorySelect.innerHTML = '<option value="">Сначала выберите категорию</option>';
//     subcategorySelect.disabled = true;
//     
//     if (selectedType) {
//         // Получаем категории для выбранного типа
//         const allowedCategories = filterData.typeflows_and_categories[selectedType] || [];
//         categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
//         fillSelect(categorySelect, allowedCategories);
//         categorySelect.disabled = allowedCategories.length === 0;
//         
//         // Восстанавливаем выбранное значение при начальной загрузке
//         if (isInitialLoad && currentCategory && allowedCategories.includes(currentCategory)) {
//             categorySelect.value = currentCategory;
//             updateSubcategories(currentCategory, true);
//         }
//     } else {
//         categorySelect.disabled = true;
//     }
// }
//
// // Вынесем обновление подкатегорий в отдельную функцию
// function updateSubcategories(selectedCategory, isInitialLoad = false) {
//     const subcategorySelect = document.getElementById('subcategory');
//     
//     // Сохраняем текущее значение перед обновлением
//     const currentSubcategory = isInitialLoad ? subcategorySelect.value : null;
//     
//     subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
//     
//     if (selectedCategory) {
//         const allowedSubcategories = filterData.categories_and_subcategories[selectedCategory] || [];
//         fillSelect(subcategorySelect, allowedSubcategories);
//         subcategorySelect.disabled = allowedSubcategories.length === 0;
//         
//         // Восстанавливаем выбранное значение при начальной загрузке
//         if (isInitialLoad && currentSubcategory && allowedSubcategories.includes(currentSubcategory)) {
//             subcategorySelect.value = currentSubcategory;
//         }
//     } else {
//         subcategorySelect.disabled = true;
//     }
// }




// ======= Управление формой редактирования записи =======
async function controlFormUpdateFlow() {
    filterData = await getStructureData();
    
    // Элементы формы
    const typeflowSelect = document.getElementById('typeflow');
    const categorySelect = document.getElementById('category');
    const subcategorySelect = document.getElementById('subcategory');
    const statusSelect = document.getElementById('status');


    // Сохраняем значения полей при первой загрузке
    const startTypeflow = typeflowSelect.value;
    const startCategory = categorySelect.value;
    const startSubcategory = subcategorySelect.value;


    // Ограничение списка категорий в выпадающем списке при загрузке странички
    // Получаем разрешенные категории для текущего типа
    const allowedCategoryIds = filterData.typeflows_and_categories[startTypeflow];
    const allowedCategories = {};
    allowedCategoryIds.forEach(id => {
        allowedCategories[id] = filterData.categories[id];
    });
    // Заполняем категории, сохраняя текущее выбранное значение
    fillSelect(categorySelect, allowedCategories);
    // Восстанавливаем первоначальную категорию
    categorySelect.value = startCategory;
    

    // Ограничение подкатегорий в выпадающем списке
    // Получаем разрешенные подкатегории для текущей категории
    const allowedSubcategoryIds = filterData.categories_and_subcategories[startCategory];
    const allowedSubcategories = {};
    allowedSubcategoryIds.forEach(id => {
        allowedSubcategories[id] = filterData.subcategories[id];
    });
    // Заполняем подкатегории, сохраняя текущее выбранное значение
    fillSelect(subcategorySelect, allowedSubcategories);
    // Восстанавливаем первоначальную подкатегорию
    subcategorySelect.value = startSubcategory;


    // Обработчик изменения типа
    typeflowSelect.addEventListener('change', function() {

        // Сбрасываем категорию и подкатегорию
        categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
        subcategorySelect.innerHTML = '<option value="">Сначала выберите категорию</option>';
        subcategorySelect.disabled = true;

        if (this.value) {
            // Получаем разрешенные категории для выбранного типа
            const allowedCategoryIds = filterData.typeflows_and_categories[this.value];
            const allowedCategories = {};

            // Фильтруем категории
            allowedCategoryIds.forEach(id => {
                allowedCategories[id] = filterData.categories[id];
            });

            // Заполняем категории
            fillSelect(categorySelect, allowedCategories);
            categorySelect.disabled = false; 
        } else {
            categorySelect.innerHTML = '<option value="">Сначала выберите тип</option>';
            categorySelect.disabled = true;
        }
    });


    // Обработчик изменения категории
    categorySelect.addEventListener('change', function() {
        if (this.value) {
            // Получаем разрешенные подкатегории
            const allowedSubcategoryIds = filterData.categories_and_subcategories[this.value];
            const allowedSubcategories = {};

            allowedSubcategoryIds.forEach(id => {
                allowedSubcategories[id] = filterData.subcategories[id];
            });
          
            // Заполняем подкатегории
            fillSelect(subcategorySelect, allowedSubcategories);
            subcategorySelect.disabled = false;
        } else {
            subcategorySelect.innerHTML = '<option value="">Сначала выберите категорию</option>';
            subcategorySelect.disabled = true;
        }
    });

}

// ======= Скрипты для соответсвующих страниц =======
document.addEventListener('DOMContentLoaded', function() {
    // Определяем текущую страницу
    if (document.getElementById('form-filter-list-flow')) {
        fillDropdownLists();
    }
    if (document.getElementById('form-create-flow')) {
        fillDropdownLists();
    }

    if (document.getElementById('form-update-flow')) {
        controlFormUpdateFlow();
    }

});
