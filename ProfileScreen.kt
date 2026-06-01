import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Моделька для отображения созданных пользователем ботов в его профиле
data class MyCreatedBot(val id: String, val name: String, val emoji: String)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(onSettingsClick: () -> Unit, onEditProfileClick: () -> Unit) {
    // Тестовый список персонажей, которых этот конкретный пользователь создал сам через вкладку «Плюс»
    val myBots = listOf(
        MyCreatedBot("1", "Кот Мурлок 🐾", "🐱"),
        MyCreatedBot("2", "Кибер-Алиса 🤖", "🤖")
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Мой Профиль 👤", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Настройки приложения")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            // 1. Блок Аватарки и Имени
            Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Box(
                    modifier = Modifier
                        .size(90.dp)
                        .background(MaterialTheme.colorScheme.primaryContainer, CircleShape)
                ) {
                    Text("👤", modifier = Modifier.align(Alignment.Center), fontSize = 44.sp)
                }
                Text(text = "Создатель Персонажей", fontWeight = FontWeight.Bold, fontSize = 22.sp)
                Text(text = "@creator_ai", color = Color.Gray, fontSize = 14.sp)
            }

            // 2. Кнопка редактирования профиля
            OutlinedButton(
                onClick = onEditProfileClick,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            ) {
                Icon(Icons.Default.Edit, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Редактировать профиль")
            }

            // 3. Блок Статистики (в виде аккуратной карточки)
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    ProfileStatItem(number = "12", label = "Чаты")
                    ProfileStatItem(number = "${myBots.size}", label = "Создано AI")
                    ProfileStatItem(number = "140", label = "Лайки твитов")
                }
            }

            Divider(modifier = Modifier.padding(vertical = 4.dp))

            // 4. Заголовок для списка созданных ботов
            Text(
                text = "Моя лаборатория персонажей 🧪",
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp,
                modifier = Modifier.fillMaxWidth()
            )

            // Сетка созданных пользователем персонажей (в стиле Character.ai)
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.weight(1f).fillMaxWidth()
            ) {
                items(myBots) { bot ->
                    Card(
                        modifier = Modifier.fillMaxWidth().height(100.dp),
                        shape = RoundedCornerShape(16.dp)
                    ) {
                        Column(
                            modifier = Modifier.padding(12.dp).fillMaxSize(),
                            verticalArrangement = Arrangement.Center,
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(bot.emoji, fontSize = 28.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(bot.name, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, maxLines = 1)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ProfileStatItem(number: String, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = number, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = MaterialTheme.colorScheme.primary)
        Text(text = label, color = Color.Gray, fontSize = 12.sp)
    }
}
