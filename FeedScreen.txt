import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.font.FontWeight

data class Post(
    val id: String,
    val characterName: String,
    val avatarUrl: String,
    val content: String,
    val likes: Int
)

@Composable
fun FeedScreen(posts: List<Post>, onCommentClick: (Post) -> Unit) {
    Scaffold(
        topBar = {
            SmallTopAppBar(title = { Text("Лента Персонажей 🐦") })
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(paddingValues),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(posts) { post ->
                PostCard(post = post, onCommentClick = { onCommentClick(post) })
            }
        }
    }
}

@Composable
fun PostCard(post: Post, onCommentClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(40.dp).clip(CircleShape).padding(4.dp)) {
                    Text("🤖", modifier = Modifier.align(Alignment.Center))
                }
                Spacer(modifier = Modifier.width(12.dp))
                Text(text = post.characterName, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = post.content)
            Spacer(modifier = Modifier.height(12.dp))
            Row {
                TextButton(onClick = { }) { Text("❤️ ${post.likes}") }
                Spacer(modifier = Modifier.width(8.dp))
                Button(onClick = onCommentClick) { Text("Ответить 💬") }
            }
        }
    }
}
