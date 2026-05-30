import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector

// Описание структуры вкладок для нижней панели
ScreenNavItem(val route: String, val title: String, val icon: ImageVector) {
    object Feed : ScreenNavItem("feed", "Лента", Icons.Default.Home)
    object Chats : ScreenNavItem("chats", "Чаты", Icons.Default.Email)
    object Create : ScreenNavItem("create", "Создать", Icons.Default.AddCircle)
    object Recommend : ScreenNavItem("recommend", "Предложки", Icons.Default.Star)
    object Profile : ScreenNavItem("profile", "Профиль", Icons.Default.AccountCircle)
}

@Composable
fun MainScreenApp() {
    var currentScreen by remember { mutableStateOf<ScreenNavItem>(ScreenNavItem.Feed) }
    val items = listOf(
        ScreenNavItem.Feed,
        ScreenNavItem.Chats,
        ScreenNavItem.Create,
        ScreenNavItem.Recommend,
        ScreenNavItem.Profile
    )

    Scaffold(
        bottomBar = {
            NavigationBar {
                items.forEach { screen ->
                    NavigationBarItem(
                        icon = { Icon(screen.icon, contentDescription = screen.title) },
                        label = { Text(screen.title) },
                        selected = currentScreen == screen,
                        onClick = { currentScreen = screen }
                    )
                }
            }
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            // Переключатель экранов на основе выбранной вкладки
            when (currentScreen) {
                is ScreenNavItem.Feed -> {
                    // Здесь будет отображаться наша Лента (FeedScreen)
                    Text("Тут будет лента постов ИИ 🐦")
                }
                is ScreenNavItem.Chats -> {
                    // Здесь будет отображаться наш список чатов (ChatsScreen)
                    Text("Тут будут ваши чаты и шкала настроения 💬")
                }
                is ScreenNavItem.Create -> {
                    Text("Экран создания нового персонажа ➕")
                }
                is ScreenNavItem.Recommend -> {
                    Text("Подборка персонажей по интересам 🎯")
                }
                is ScreenNavItem.Profile -> {
                    Text("Ваш личный профиль и настройки 👤")
                }
            }
        }
    }
}
