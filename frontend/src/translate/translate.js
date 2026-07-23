export const messages = {
  ru: {
    header: {
      logoTitle: 'На главную',
      greeting: 'Привет',
      builderBtn: 'Конструктор',
      profileBtn: 'Мой профиль',
      logoutBtn: 'Выйти',
      loginBtn: 'Войти'
    },
    builder: {
      step1_title: 'Шаг 1: Основа системы',
      step2_title: 'Шаг 2: Память и Видео',
      step3_title: 'Шаг 3: Корпус и Питание',
      summary_title: 'Итоговая сборка',
      labels: {
        cpu: 'Процессор (CPU)', mb: 'Материнская плата', cooler: 'Охлаждение',
        ram: 'Оперативная память', gpu: 'Видеокарта', psu: 'Блок питания', case: 'Корпус'
      },
      filters: {allBrands: 'Все бренды', 
                minPrice: 'Мин. ₴', 
                maxPrice: 'Макс. ₴', 
                minW: 'Мин. W', 
                sortDefault: 'Сортировка', 
                sortAsc: 'Сначала дешевые', 
                sortDesc: 'Сначала дорогие'},
      placeholders: {
        selectCpu: '-- Выберите процессор --', needCpuFirst: 'Сначала выберите процессор',
        selectMb: '-- Выберите материнскую плату --', needMbFirst: 'Сначала выберите материнскую плату',
        selectCooler: '-- Выберите охлаждение --', selectRam: '-- Выберите оперативную память --',
        selectGpu: '-- Выберите видеокарту --', selectPsu: '-- Выберите блок питания --',
        selectCase: '-- Выберите корпус --'
      },
      hints: {
        mbHint: 'Отображаются только платы с подходящим сокетом',
        tdpHint: 'TDP Сборки: {tdp} Вт. Рекомендуем БП от {psu} Вт.' 
      },
      summary: {
        empty: 'Сборка пуста. Выберите комплектующие слева.',
        noPhoto: 'Нет<br>фото', remove: 'Убрать из сборки', total: 'Итого:',
        tdp: 'Потребление (TDP):', saveBtn: 'Сохранить сборку'
      }
    },
    profile: {
      settingsTitle: 'Настройки профиля', newUsername: 'Новое имя пользователя',
      newPassword: 'Новый пароль', leaveEmpty: 'Оставьте пустым, если не меняете',
      saveChanges: 'Сохранить изменения', passwordWarning: 'Внимание: при смене пароля потребуется войти заново!',
      buildsTitle: 'Мои сохраненные сборки', noBuilds: 'У вас пока нет сохраненных сборок.',
      deleteHint: 'Удалить сборку', openBuilder: 'Открыть в конструкторе',
      createdAt: 'Создана:', recently: 'Недавно'
    },
    auth: {
      loginTitle: 'Вход в аккаунт', registerTitle: 'Регистрация',
      username: 'Имя пользователя (Логин)', email: 'Email', password: 'Пароль',
      loginBtn: 'Войти', registerBtn: 'Зарегистрироваться', noAccount: 'Нет аккаунта?',
      hasAccount: 'Уже есть аккаунт?', createBtn: 'Создать'
    },
    modals: {
      save: {
          titleUpdate: 'Обновление сборки', titleSave: 'Сохранение сборки', buildNameLabel: 'Название сборки', 
          buildNamePlaceholder: 'Моя супер сборка', updateCurrent: 'Обновить текущую', 
          saveAsNew: 'Сохранить как новую', saveBtn: 'Сохранить', 
          clearBuild: 'Очистить зборку'
        },

      delete: { 
        title: 'Удалить сборку?', description: 'Это действие невозможно отменить. Вы действительно хотите удалить конфигурацию?',
        cancel: 'Отмена', confirm: 'Удалить' 
      }
    }, 
  },

  uk: {
    header: {
      logoTitle: 'На головну',
      greeting: 'Привіт',
      builderBtn: 'Конструктор',
      profileBtn: 'Мій профіль',
      logoutBtn: 'Вийти',
      loginBtn: 'Увійти'
    },
    builder: {
      step1_title: 'Крок 1: Основа системи',
      step2_title: 'Крок 2: Пам\'ять та Відео',
      step3_title: 'Крок 3: Корпус та Живлення',
      summary_title: 'Підсумкова збірка',
      labels: {
        cpu: 'Процесор (CPU)', mb: 'Материнська плата', cooler: 'Охолодження',
        ram: 'Оперативна пам\'ять', gpu: 'Відеокарта', psu: 'Блок живлення', case: 'Корпус'
      },
      filters: {allBrands: 'Всі бренды', 
                minPrice: 'Мін. ₴', 
                maxPrice: 'Макс. ₴', 
                minW: 'Мін. W', 
                sortDefault: 'Сортировка', 
                sortAsc: 'Спочатку дешеві', 
                sortDesc: 'Спочатку дорогі'},
      placeholders: {
        selectCpu: '-- Оберіть процесор --', needCpuFirst: 'Спочатку оберіть процесор',
        selectMb: '-- Оберіть материнську плату --', needMbFirst: 'Спочатку оберіть материнську плату',
        selectCooler: '-- Оберіть охолодження --', selectRam: '-- Оберіть оперативну пам\'ять --',
        selectGpu: '-- Оберіть відеокарту --', selectPsu: '-- Оберіть блок живлення --',
        selectCase: '-- Оберіть корпус --'
      },
      hints: {
        mbHint: 'Відображаються лише плати з відповідним сокетом',
        tdpHint: 'TDP Збірки: {tdp} Вт. Рекомендуємо БЖ від {psu} Вт.' 
      },
      summary: {
        empty: 'Збірка порожня. Оберіть комплектуючі зліва.',
        noPhoto: 'Немає<br>фото', remove: 'Прибрати зі збірки', total: 'Разом:',
        tdp: 'Споживання (TDP):', saveBtn: 'Зберегти збірку'
      }
    },
    profile: {
      settingsTitle: 'Налаштування профілю', newUsername: 'Нове ім\'я користувача',
      newPassword: 'Новий пароль', leaveEmpty: 'Залиште порожнім, якщо не змінюєте',
      saveChanges: 'Зберегти зміни', passwordWarning: 'Увага: при зміні пароля потрібно буде увійти заново!',
      buildsTitle: 'Мої збережені збірки', noBuilds: 'У вас поки немає збережених збірок.',
      deleteHint: 'Видалити збірку', openBuilder: 'Відкрити в конструкторі',
      createdAt: 'Створена:', recently: 'Нещодавно'
    },
    auth: {
      loginTitle: 'Вхід в акаунт', registerTitle: 'Реєстрація',
      username: 'Ім\'я користувача (Логін)', email: 'Email', password: 'Пароль',
      loginBtn: 'Увійти', registerBtn: 'Зареєструватися', noAccount: 'Немає акаунту?',
      hasAccount: 'Вже є акаунт?', createBtn: 'Створити'
    },
    modals: {
      save: {
          titleUpdate: 'Оновлення збірки', titleSave: 'Збереження збірки', buildNameLabel: 'Назва збірки', 
          buildNamePlaceholder: 'Моя супер збірка', updateCurrent: 'Оновити поточну', 
          saveAsNew: 'Зберегти як нову', saveBtn: 'Зберегти', 
          clearBuild: 'Очистити збірку'
        },

      delete: { 
        title: 'Видалити збірку?', description: 'Цю дію неможливо відмінити. Ви дійсно хочете це зробити?',
        cancel: 'Скасувати', confirm: 'Відалити' 
      }
    }
  },

  en: {
    header: {
      logoTitle: 'To Home',
      greeting: 'Hello',
      builderBtn: 'Builder',
      profileBtn: 'My Profile',
      logoutBtn: 'Logout',
      loginBtn: 'Login'
    },
    builder: {
      step1_title: 'Step 1: Core System',
      step2_title: 'Step 2: Memory and Video',
      step3_title: 'Step 3: Case and Power',
      summary_title: 'Build Summary',
      labels: {
        cpu: 'Processor (CPU)', mb: 'Motherboard', cooler: 'Cooler',
        ram: 'RAM', gpu: 'Video Card (GPU)', psu: 'Power Supply (PSU)', case: 'Case'
      },
      filters: {allBrands: 'All brands', 
                minPrice: 'Min. ₴', 
                maxPrice: 'Max. ₴', 
                minW: 'Min. W', 
                sortDefault: 'Sort by', 
                sortAsc: 'Price: Low to High', 
                sortDesc: 'Price: High to Low'},
      placeholders: {
        selectCpu: '-- Select CPU --', needCpuFirst: 'Select a CPU first',
        selectMb: '-- Select Motherboard --', needMbFirst: 'Select a Motherboard first',
        selectCooler: '-- Select Cooler --', selectRam: '-- Select RAM --',
        selectGpu: '-- Select GPU --', selectPsu: '-- Select PSU --',
        selectCase: '-- Select Case --'
      },
      hints: {
        mbHint: 'Only motherboards with a compatible socket are shown',
        tdpHint: 'Build TDP: {tdp} W. Recommended PSU: {psu} W or more.' 
      },
      summary: {
        empty: 'Build is empty. Select components on the left.',
        noPhoto: 'No<br>photo', remove: 'Remove from build', total: 'Total:',
        tdp: 'Power Consumption (TDP):', saveBtn: 'Save Build'
      }
    },
    profile: {
      settingsTitle: 'Profile Settings', newUsername: 'New username',
      newPassword: 'New password', leaveEmpty: 'Leave empty if not changing',
      saveChanges: 'Save Changes', passwordWarning: 'Note: changing your password will require you to log in again!',
      buildsTitle: 'My Saved Builds', noBuilds: 'You have no saved builds yet.',
      deleteHint: 'Delete build', openBuilder: 'Open in builder',
      createdAt: 'Created:', recently: 'Recently'
    },
    auth: {
      loginTitle: 'Account Login', registerTitle: 'Registration',
      username: 'Username (Login)', email: 'Email', password: 'Password',
      loginBtn: 'Login', registerBtn: 'Register', noAccount: 'No account?',
      hasAccount: 'Already have an account?', createBtn: 'Create one'
    }, 
    modals: {
      save: {
          titleUpdate: 'Build update', titleSave: 'Build save', buildNameLabel: 'Build name', 
          buildNamePlaceholder: 'My Super PC', updateCurrent: 'Update current', 
          saveAsNew: 'Save as new', saveBtn: 'Save',
          clearBuild: 'Clear build'
        },

      delete: { 
        title: 'Delete build?', description: 'This action cannot be undone. Are you sure you want to delete this configuration?',
        cancel: 'Cancel', confirm: 'Delete' 
      }
    },
  }
};