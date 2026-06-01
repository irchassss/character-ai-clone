import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CallEnd
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

@Composable
fun VoiceCallScreen(characterName: String, onDisconnectClick: () -> Unit) {
    var secondsConnected by remember { mutableStateOf(0) }

    // Секундомер времени разговора (увеличивается каждую секунду)
    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            secondsConnected++
        }
    }

    // Форматируем время в красивый вид (например, 01:23)
    val minutes = secondsConnected / 60
    val seconds = secondsConnected % 60
    val timeString = String.format("%02d:%02d", minutes, seconds)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF1A1A1A)) // Красивый темный фон, как при реальном звонке
            .padding(32.dp)
    ) {
        Column(
            modifier = Modifier.align(Alignment.TopCenter).padding(top = 64.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Крупное имя персонажа
            Text(text = characterName, color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
            
            // Время разговора
            Text(text = timeString, color = Color.LightGray, fontSize = 18.sp)
        }

        // Круглая аватарка персонажа по центру экрана
        Box(
            modifier = Modifier
                .size(160.dp)
                .background(Color.DarkGray, CircleShape)
                .align(Alignment.Center)
        ) {
            Text(text = "🐾", modifier = Modifier.align(Alignment.Center), fontSize = 64.sp)
        }

        // НАША ФИШКА: Красная кнопка с трубкой для завершения вызова в самом низу
        Button(
            onClick = onDisconnectClick,
            colors = ButtonDefaults.buttonColors(containerColor = Color.Red),
            shape = CircleShape,
            modifier = Modifier
                .size(72.dp)
                .align(Alignment.BottomCenter)
                .padding(bottom = 16.dp),
            contentPadding = PaddingValues(0.dp)
        ) {
            Icon(
                imageVector = Icons.Default.CallEnd,
                contentDescription = "Завершить вызов",
                tint = Color.White,
                modifier = Modifier.size(36.dp)
            )
        }
    }
}
