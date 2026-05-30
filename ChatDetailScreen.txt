import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class Message(val text: String, val isUser: Boolean)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatDetailScreen(characterName: String, onPhoneClick: () -> Unit, onBackClick: () -> Unit) {
    var messageText by remember { mutableStateOf("") }
    val messages = remember { mutableStateListOf(
        Message("Привет! Я ворчливый кот Мурлок. Опять баги пишешь? 🐾", isUser = false)
    ) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(characterName, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBackClick) { Icon(Icons.Default.ArrowBack, "Назад") }
                },
                actions = {
                    // НАША ФИШКА: Иконка телефона в правом верхнем углу
                    IconButton(onClick = onPhoneClick) {
                        Icon(Icons.Default.Phone, contentDescription = "Позвонить", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
            // Лента сообщений мессенджера
            LazyColumn(
                modifier = Modifier.weight(1f).fillMaxWidth().padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(messages) { message ->
                    val alignment = if (message.isUser) Alignment.End else Alignment.Start
                    val color = if (message.isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer
                    
                    Box(modifier = Modifier.fillMaxWidth(), contentAlignment = alignment) {
                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = color,
                            modifier = Modifier.widthIn(max = 280.dp)
                        ) {
                            Text(text = message.text, modifier = Modifier.padding(12.dp), fontSize = 16.sp)
                        }
                    }
                }
            }

            // Нижнее поле ввода и кнопка отправки
            Row(
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedTextField(
                    value = messageText,
                    onValueChange = { messageText = it },
                    placeholder = { Text("Напишите персонажу...") },
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(24.dp)
                )
                FloatingActionButton(
                    onClick = {
                        if (messageText.isNotBlank()) {
                            messages.add(Message(messageText, isUser = true))
                            messageText = ""
                            // Сюда позже пойдет запрос к нашему серверу Render
                        }
                    },
                    shape = RoundedCornerShape(24.dp)
                ) {
                    Icon(Icons.Default.Send, "Отправить")
                }
            }
        }
    }
}
