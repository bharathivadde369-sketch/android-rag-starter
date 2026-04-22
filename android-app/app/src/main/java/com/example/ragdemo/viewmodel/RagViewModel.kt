package com.example.ragdemo.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.ragdemo.data.repository.RagRepository
import com.example.ragdemo.ui.state.RagUiState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class RagViewModel(
    private val repository: RagRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(RagUiState())
    val uiState: StateFlow<RagUiState> = _uiState

    fun onQueryChange(value: String) {
        _uiState.update { it.copy(query = value) }
    }

    fun ask() {
        val query = _uiState.value.query.trim()
        if (query.isEmpty()) return

        viewModelScope.launch {
            _uiState.update {
                it.copy(isLoading = true, error = null, answer = "", matchedContext = "")
            }

            repository.ask(query)
                .onSuccess { response ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            answer = response.answer,
                            matchedContext = response.matchedContext
                        )
                    }
                }
                .onFailure { throwable ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = throwable.message ?: "Unknown error"
                        )
                    }
                }
        }
    }
}
