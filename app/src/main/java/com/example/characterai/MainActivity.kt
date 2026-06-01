package com.example.characterai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                SimpleScreen()
            }
        }
    }
}

@Composable
fun SimpleScreen() {
    var text by remember { mutableStateOf("Hello! Character AI работает!") }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.headlineMedium
        )
        Button(
            onClick = { text = "Приложение запустилось успешно! 🎉" },
            modifier = Modifier.padding(top = 16.dp)
        ) {
            Text("Нажми меня")
        }
    }
}
