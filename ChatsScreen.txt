import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class ChatItem(
    val id: String,
    val name: String,
    val lastMessage: String,
    val time: String,
    val mood: Int,
    val unreadCount: Int
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatsScreen(onChatClick: (ChatItem) -> Unit) {
    var searchQuery by remember { mutableStateOf("") }
    val testChats = listOf(
        ChatItem("1", "Кот Мурлок 🐾", "Ты опять написал баг?", "14:40", 35, 2),
        ChatItem("2", "Кибер-Алиса 🤖", "Голосовой вызов доступен.", "Вчера", 80, 0)
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Чаты 💬", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = { }) { Icon(Icons.Default.Search, null) }
                    Box {
                        IconButton(onClick = { }) { Icon(Icons.Default.Notifications, null) }
                        Box(modifier = Modifier.size(18.dp).background(Color.Red, CircleShape).align(Alignment.TopEnd)) {
                            Text("3", color = Color.White, fontSize = 10.sp, modifier = Modifier.align(Alignment.Center))
                        }
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                placeholder = { Text("Поиск персонажа...") },
                leadingIcon = { Icon(Icons.Default.Search, null) },
                shape = RoundedCornerShape(12.dp)
            )
            LazyColumn(modifier = Modifier.fillMaxSize()) {
                items(testChats.filter { it.name.contains(searchQuery, ignoreCase = true) }) { chat ->
                    ChatRow(chat = chat, onClick = { onChatClick(chat) })
                }
            }
        }
    }
}

@Composable
fun ChatRow(chat: ChatItem, onClick: () -> Unit) {
    Surface(onClick = onClick, modifier = Modifier.fillMaxWidth()) {
        Row(modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(50.dp).background(Color.LightGray, CircleShape)) {
                Text("🤖", modifier = Modifier.align(Alignment.Center), fontSize = 24.sp)
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1.1f)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(text = chat.name, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text(text = chat.time, color = Color.Gray, fontSize = 12.sp)
                }
                Text(text = chat.lastMessage, color = Color.Gray, maxLines = 1, fontSize = 14.sp)
                Spacer(modifier = Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Настроение: ", fontSize = 11.sp, color = Color.Gray)
                    LinearProgressIndicator(
                        progress = chat.mood / 100f,
                        modifier = Modifier.weight(1f).height(6.dp).clip(RoundedCornerShape(3.dp)),
                        color = if (chat.mood > 50) Color.Green else Color.Red,
                        trackColor = Color.LightGray
                    )
                }
            }
        }
    }
}
