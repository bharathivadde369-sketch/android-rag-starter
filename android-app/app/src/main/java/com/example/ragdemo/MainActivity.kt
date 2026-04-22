package com.example.ragdemo

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import com.example.ragdemo.data.remote.RetrofitProvider
import com.example.ragdemo.data.repository.RagRepository
import com.example.ragdemo.ui.screen.RagScreen
import com.example.ragdemo.ui.theme.RagDemoTheme
import com.example.ragdemo.viewmodel.RagViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val repository = RagRepository(RetrofitProvider.apiService)
        val viewModel = RagViewModel(repository)

        setContent {
            RagDemoTheme {
                Surface(color = MaterialTheme.colorScheme.background) {
                    RagScreen(viewModel)
                }
            }
        }
    }
}
