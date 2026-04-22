package com.example.ragdemo.ui.state

data class RagUiState(
    val query: String = "",
    val answer: String = "",
    val matchedContext: String = "",
    val isLoading: Boolean = false,
    val error: String? = null
)
