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

// Вспомогательная функция для заполнения выпадающих списков
function fillSelect(selectElement, options) {
    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        selectElement.appendChild(opt);
    });
}


// ======= Заполнение выпадающих списков  =======
async function fillDropdownLists() {
    filterData = await getStructureData();
    
    // Элементы формы
    const typeflowSelect = document.getElementById('typeflow');
    const categorySelect = document.getElementById('category');
    const subcategorySelect = document.getElementById('subcategory');
    const statusSelect = document.getElementById('status');

    // Заполняем статичные поля
    fillSelect(typeflowSelect, filterData.typeflows);
    fillSelect(statusSelect, filterData.statuses);

    // Если форма редактирования и есть выбранный тип
    if (typeflowSelect.value && document.getElementById('form-update-flow')) {
        updateCategories(typeflowSelect.value, true);
    }

    // Обработчик изменения типа
    typeflowSelect.addEventListener('change', function() {
        updateCategories(this.value);
    });

    // Если форма редактирования и есть выбранная категория
    if (categorySelect.value && document.getElementById('form-update-flow')) {
        updateSubcategories(categorySelect.value, true);
    }

    // Обработчик изменения категории
    categorySelect.addEventListener('change', function() {
        updateSubcategories(this.value);
    });
}

// Вынесем обновление категорий в отдельную функцию
function updateCategories(selectedType, isInitialLoad = false) {
    const categorySelect = document.getElementById('category');
    const subcategorySelect = document.getElementById('subcategory');
    
    // Сохраняем текущее значение перед обновлением
    const currentCategory = isInitialLoad ? categorySelect.value : null;
    
    // Сбрасываем подкатегории
    subcategorySelect.innerHTML = '<option value="">Сначала выберите категорию</option>';
    subcategorySelect.disabled = true;
    
    if (selectedType) {
        // Получаем категории для выбранного типа
        const allowedCategories = filterData.typeflows_and_categories[selectedType] || [];
        categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
        fillSelect(categorySelect, allowedCategories);
        categorySelect.disabled = allowedCategories.length === 0;
        
        // Восстанавливаем выбранное значение при начальной загрузке
        if (isInitialLoad && currentCategory && allowedCategories.includes(currentCategory)) {
            categorySelect.value = currentCategory;
            updateSubcategories(currentCategory, true);
        }
    } else {
        categorySelect.disabled = true;
    }
}

// Вынесем обновление подкатегорий в отдельную функцию
function updateSubcategories(selectedCategory, isInitialLoad = false) {
    const subcategorySelect = document.getElementById('subcategory');
    
    // Сохраняем текущее значение перед обновлением
    const currentSubcategory = isInitialLoad ? subcategorySelect.value : null;
    
    subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
    
    if (selectedCategory) {
        const allowedSubcategories = filterData.categories_and_subcategories[selectedCategory] || [];
        fillSelect(subcategorySelect, allowedSubcategories);
        subcategorySelect.disabled = allowedSubcategories.length === 0;
        
        // Восстанавливаем выбранное значение при начальной загрузке
        if (isInitialLoad && currentSubcategory && allowedSubcategories.includes(currentSubcategory)) {
            subcategorySelect.value = currentSubcategory;
        }
    } else {
        subcategorySelect.disabled = true;
    }
}

// ======= Инициализация =======
document.addEventListener('DOMContentLoaded', function() {
    // Определяем текущую страницу
    if (document.getElementById('filter-form-list-flow')) {
        fillDropdownLists();
    }
    if (document.getElementById('create-form-flow')) {
        fillDropdownLists();
    }

    if (document.getElementById('form-update-flow')) {
        fillDropdownLists();
    }

});
