package com.example.characterai
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
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

// Архитектурное описание вкладок нижней панели навигации
sealed class AppScreen(val route: String, val title: String, val icon: ImageVector) {
    object Feed : AppScreen("feed", "Лента", Icons.Default.Home)
    object Chats : AppScreen("chats", "Чаты", Icons.Default.Email)
    object Create : AppScreen("create", "Создать", Icons.Default.AddCircle)
    object Recommend : AppScreen("recommend", "Предложки", Icons.Default.Star)
    object Profile : AppScreen("profile", "Профиль", Icons.Default.AccountCircle)
    
    // Скрытые экраны для глубоких переходов (вне нижней панели)
    object ChatDetail : AppScreen("chat_detail", "Диалог", Icons.Default.Email)
    object VoiceCall : AppScreen("voice_call", "Звонок", Icons.Default.Email)
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                MainAppNavigationController()
            }
        }
    }
}

@Composable
fun MainAppNavigationController() {
    // Храним текущий открытый экран и данные выбранного персонажа
    var currentScreen by remember { mutableStateOf<AppScreen>(AppScreen.Feed) }
    var selectedCharacterName by remember { mutableStateOf("Кот Мурлок 🐾") }

    val bottomNavigationItems = listOf(
        AppScreen.Feed,
        AppScreen.Chats,
        AppScreen.Create,
        AppScreen.Recommend,
        AppScreen.Profile
    )

    Scaffold(
        // Нижняя панель отображается ТОЛЬКО на основных вкладках. На экране звонка она скрыта!
        bottomBar = {
            if (currentScreen != AppScreen.VoiceCall) {
                NavigationBar {
                    bottomNavigationItems.forEach { screen ->
                        NavigationBarItem(
                            icon = { Icon(screen.icon, contentDescription = screen.title) },
                            label = { Text(screen.title) },
                            selected = (currentScreen == screen || (screen == AppScreen.Chats && currentScreen == AppScreen.ChatDetail)),
                            onClick = { currentScreen = screen }
                        )
                    }
                }
            }
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            // Центральный переключатель всей логики интерфейса приложения
            when (currentScreen) {
                is AppScreen.Feed -> {
                    // Подключаем нашу Твиттер-ленту ИИ (из файла FeedScreen.txt)
                    FeedScreen(posts = emptyList(), onCommentClick = { _ -> 
                        // Логика перехода к ветке комментариев к посту
                    })
                }
                is AppScreen.Chats -> {
                    // Подключаем список активных чатов (из файла ChatsScreen.txt)
                    ChatsScreen(onChatClick = { chatItem ->
                        selectedCharacterName = chatItem.name
                        currentScreen = AppScreen.ChatDetail // Переходим внутрь диалога при клике на бота
                    })
                }
                is AppScreen.ChatDetail -> {
                    // Подключаем экран мессенджера (из файла ChatDetailScreen.txt)
                    ChatDetailScreen(
                        characterName = selectedCharacterName,
                        onPhoneClick = { currentScreen = AppScreen.VoiceCall }, // По клику на трубку — звоним!
                        onBackClick = { currentScreen = AppScreen.Chats }
                    )
                }
                is AppScreen.VoiceCall -> {
                    // НАША ГЛАВНАЯ ФИШКА: Экран голосового звонка (из файла VoiceCallScreen.txt)
                    VoiceCallScreen(
                        characterName = selectedCharacterName,
                        onDisconnectClick = { currentScreen = AppScreen.ChatDetail } // Сброс трубки возвращает в чат
                    )
                }
                is AppScreen.Create -> {
                    // Подключаем конструктор создания ботов (из файла CreateCharacterScreen.txt)
                    CreateCharacterScreen(onCharacterCreated = { name, prompt, mood ->
                        // Сюда пойдет логика сохранения нового бота в Supabase
                        currentScreen = AppScreen.Chats
                    })
                }
                is AppScreen.Recommend -> {
                    // Подключаем вкладку предложек (из файла RecommendationsScreen.txt)
                    RecommendationsScreen(onBotClick = { recommendedBot ->
                        selectedCharacterName = recommendedBot.name
                        currentScreen = AppScreen.ChatDetail
                    })
                }
                is AppScreen.Profile -> {
                    // Подключаем вкладку Профиля (из файла ProfileScreen.txt)
                    ProfileScreen(onSettingsClick = {}, onEditProfileClick = {})
                }
            }
        }
    }
}
