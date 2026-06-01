import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Моделька для карточки рекомендации
data class RecommendedBot(val id: String, val name: String, val description: str, val emoji: String)

@Composable
fun RecommendationsScreen(onBotClick: (RecommendedBot) -> Unit) {
    // Тестовые подборки по категориям, которые подходят по интересам человеку
    val popularBots = listOf(
        RecommendedBot("1", "Кот Мурлок 🐾", "Ворчливый кот-программист", "🐱"),
        RecommendedBot("3", "Эльф Лиадон 🏹", "Фэнтези-проводник и наставник", "🧝‍♂️")
    )
    
    val helperBots = listOf(
        RecommendedBot("4", "Профи Английского 🇬🇧", "Твой личный репетитор", "👨‍🏫"),
        RecommendedBot("5", "Психолог Макс 🧠", "Поговорим обо всем и снимем стресс", "🛋️")
    )

    Scaffold(
        topBar = {
            SmallTopAppBar(title = { Text("Предложки для вас 🎯", fontWeight = FontWeight.Bold) })
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            Text("Подобрано на основе ваших интересов", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)

            // Категория 1: Популярные сейчас
            CategorySection(title = "🔥 Популярные персонажи", bots = popularBots, onBotClick = onBotClick)

            // Категория 2: Помощники в учебе и жизни
            CategorySection(title = "📚 Помощники и Менторы", bots = helperBots, onBotClick = onBotClick)
        }
    }
}

@Composable
fun CategorySection(title: str, bots: List<RecommendedBot>, onBotClick: (RecommendedBot) -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text(text = title, fontWeight = FontWeight.Bold, fontSize = 18.sp)
        LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            items(bots) { bot ->
                BotRecommendationCard(bot = bot, onClick = { onBotClick(bot) })
            }
        }
    }
}

@Composable
fun BotRecommendationCard(bot: RecommendedBot, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        modifier = Modifier.width(160.dp).height(180.dp)
    ) {
        Column(
            modifier = Modifier.padding(12.dp).fillMaxSize(),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Text(bot.emoji, fontSize = 32.sp)
            Column {
                Text(bot.name, fontWeight = FontWeight.Bold, maxLines = 1, fontSize = 14.sp)
                Spacer(modifier = Modifier.height(4.dp))
                Text(bot.description, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2, fontSize = 12.sp)
            }
        }
    }
}
