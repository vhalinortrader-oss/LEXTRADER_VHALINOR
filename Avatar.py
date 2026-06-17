import streamlit as st
import time
import random
import threading
import asyncio
import json
import numpy as np
from datetime import datetime, timedelta
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Callable, Tuple
import queue
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import os
from pathlib import Path
import base64
from math import sin, cos, pi
from collections import deque
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ==================== ENUMS E TIPOS ====================
class Emotion(Enum):
    NEUTRAL = ("neutral", "#06b6d4")
    HAPPY = ("happy", "#10b981")
    EXCITED = ("excited", "#f59e0b")
    FOCUSED = ("focused", "#3b82f6")
    INTENSE = ("intense", "#8b5cf6")
    SURPRISED = ("surprised", "#f97316")
    SAD = ("sad", "#6b7280")
    ANALYZING = ("analyzing", "#6366f1")
    DEFENSIVE = ("defensive", "#ef4444")
    CALM = ("calm", "#14b8a6")
    SLEEPING = ("sleeping", "#374151")
    
    def __init__(self, emotion, color):
        self.emotion_name = emotion
        self.color = color

class AvatarState(Enum):
    ACTIVE = auto()
    SLEEPING = auto()
    LISTENING = auto()
    PROCESSING = auto()
    ALERT = auto()
    ERROR = auto()
    INITIALIZING = auto()

@dataclass
class ChatMessage:
    role: str
    text: str
    emotion: Emotion = Emotion.NEUTRAL
    timestamp: datetime = None
    data_points: Optional[Dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class AnimationFrame:
    symbols: List[str]
    colors: List[str]
    positions: List[Tuple[float, float]]
    velocities: List[Tuple[float, float]]
    lifetime: float = 1.0

# ==================== ANIMAÇÃO DE PARTÍCULAS ====================
class ParticleSystem:
    def __init__(self, max_particles=200):
        self.particles = []
        self.max_particles = max_particles
        self.last_update = time.time()
        
    def emit(self, x: float, y: float, count: int = 10, 
             color: str = "#06b6d4", symbol: str = "•", 
             velocity_range: Tuple[float, float] = (-1, 1)):
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            vx = random.uniform(*velocity_range)
            vy = random.uniform(*velocity_range)
            life = random.uniform(0.5, 1.5)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'life': life,
                'max_life': life,
                'color': color,
                'symbol': symbol,
                'size': random.uniform(0.5, 1.5)
            })
    
    def update(self, dt: float):
        current_time = time.time()
        dt = min(current_time - self.last_update, 0.033)  # Cap at 30fps
        self.last_update = current_time
        
        # Update particles
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt * 60
            p['y'] += p['vy'] * dt * 60
            p['life'] -= dt
            
            # Apply gravity and fade
            p['vy'] += 0.1 * dt * 60
            if p['life'] < p['max_life'] * 0.3:
                p['vx'] *= 0.9
                p['vy'] *= 0.9
            
            # Remove dead particles
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def render_html(self) -> str:
        if not self.particles:
            return ""
        
        particles_html = []
        for p in self.particles:
            opacity = p['life'] / p['max_life']
            size = p['size'] * (0.5 + opacity * 0.5)
            particles_html.append(
                f'<div style="position: absolute; left: {p["x"]}px; top: {p["y"]}px; '
                f'color: {p["color"]}; opacity: {opacity}; font-size: {size}rem; '
                f'transform: translate(-50%, -50%); pointer-events: none;">{p["symbol"]}</div>'
            )
        
        return ''.join(particles_html)

# ==================== SISTEMA DE ANIMAÇÃO FACIAL ====================
class FacialAnimation:
    def __init__(self):
        self.eye_state = "neutral"  # neutral, happy, focused, surprised
        self.mouth_state = "neutral" # neutral, smile, open, line
        self.brow_state = "neutral"  # neutral, raised, furrowed
        self.blink_timer = 0
        self.blink_duration = 0.1
        self.blink_interval = random.uniform(2, 5)
        self.last_blink = time.time()
        
    def update(self, emotion: Emotion):
        current_time = time.time()
        
        # Blinking logic
        if current_time - self.last_blink > self.blink_interval:
            self.eye_state = "blinking"
            self.last_blink = current_time
            self.blink_interval = random.uniform(2, 5)
        elif current_time - self.last_blink > self.blink_duration:
            self.eye_state = self.get_eye_state(emotion)
        
        # Update facial features based on emotion
        self.mouth_state = self.get_mouth_state(emotion)
        self.brow_state = self.get_brow_state(emotion)
    
    def get_eye_state(self, emotion: Emotion) -> str:
        if emotion == Emotion.HAPPY:
            return "happy"
        elif emotion == Emotion.FOCUSED or emotion == Emotion.ANALYZING:
            return "focused"
        elif emotion == Emotion.SURPRISED:
            return "surprised"
        elif emotion == Emotion.DEFENSIVE:
            return "intense"
        return "neutral"
    
    def get_mouth_state(self, emotion: Emotion) -> str:
        if emotion == Emotion.HAPPY:
            return "smile"
        elif emotion == Emotion.SURPRISED:
            return "open"
        elif emotion == Emotion.DEFENSIVE or emotion == Emotion.INTENSE:
            return "line"
        elif emotion == Emotion.SAD:
            return "sad"
        return "neutral"
    
    def get_brow_state(self, emotion: Emotion) -> str:
        if emotion == Emotion.SURPRISED:
            return "raised"
        elif emotion == Emotion.FOCUSED or emotion == Emotion.ANALYZING:
            return "furrowed"
        elif emotion == Emotion.DEFENSIVE:
            return "intense"
        return "neutral"
    
    def render_face(self, emotion: Emotion) -> str:
        self.update(emotion)
        
        # Face container
        face_html = f'<div style="position: relative; width: 64px; height: 64px;">'
        
        # Background aura
        face_html += f'''
            <div style="position: absolute; inset: -8px; border-radius: 50%; 
                  background: radial-gradient(circle, {emotion.color}22 0%, transparent 70%);
                  animation: pulse 2s ease-in-out infinite;"></div>
        '''
        
        # Face base
        face_html += f'''
            <div style="position: absolute; inset: 0; border-radius: 50%; 
                  background: linear-gradient(135deg, #1f2937, #111827); 
                  border: 2px solid {emotion.color}; box-shadow: 0 0 20px {emotion.color}44;"></div>
        '''
        
        # Eyes
        eye_y = "28px"
        if self.eye_state == "happy":
            eye_html = f'''
                <div style="position: absolute; top: {eye_y}; left: 18px; width: 8px; height: 4px; 
                      border-radius: 4px; background: {emotion.color};"></div>
                <div style="position: absolute; top: {eye_y}; right: 18px; width: 8px; height: 4px; 
                      border-radius: 4px; background: {emotion.color};"></div>
            '''
        elif self.eye_state == "focused":
            eye_html = f'''
                <div style="position: absolute; top: {eye_y}; left: 18px; width: 6px; height: 6px; 
                      border-radius: 50%; background: {emotion.color}; 
                      box-shadow: 0 0 10px {emotion.color};"></div>
                <div style="position: absolute; top: {eye_y}; right: 18px; width: 6px; height: 6px; 
                      border-radius: 50%; background: {emotion.color}; 
                      box-shadow: 0 0 10px {emotion.color};"></div>
            '''
        elif self.eye_state == "blinking":
            eye_html = f'''
                <div style="position: absolute; top: {eye_y}; left: 16px; width: 12px; height: 2px; 
                      background: {emotion.color};"></div>
                <div style="position: absolute; top: {eye_y}; right: 16px; width: 12px; height: 2px; 
                      background: {emotion.color};"></div>
            '''
        else:  # neutral
            eye_html = f'''
                <div style="position: absolute; top: {eye_y}; left: 20px; width: 4px; height: 8px; 
                      border-radius: 2px; background: {emotion.color};"></div>
                <div style="position: absolute; top: {eye_y}; right: 20px; width: 4px; height: 8px; 
                      border-radius: 2px; background: {emotion.color};"></div>
            '''
        
        face_html += eye_html
        
        # Mouth
        if self.mouth_state == "smile":
            mouth_html = f'''
                <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
                      width: 24px; height: 12px; border-bottom: 3px solid {emotion.color};
                      border-radius: 0 0 12px 12px;"></div>
            '''
        elif self.mouth_state == "open":
            mouth_html = f'''
                <div style="position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%);
                      width: 16px; height: 16px; border: 2px solid {emotion.color};
                      border-radius: 50%;"></div>
            '''
        else:  # neutral line
            mouth_html = f'''
                <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
                      width: 24px; height: 2px; background: {emotion.color};"></div>
            '''
        
        face_html += mouth_html
        
        # Glow effect
        face_html += f'''
            <div style="position: absolute; inset: -4px; border-radius: 50%; 
                  background: radial-gradient(circle at center, {emotion.color}33 0%, transparent 70%);
                  animation: glow 3s ease-in-out infinite alternate;"></div>
        '''
        
        face_html += '</div>'
        
        return face_html

# ==================== SISTEMA DE GESTOS ====================
class GestureSystem:
    def __init__(self):
        self.current_gesture = "idle"
        self.gesture_timer = 0
        self.gesture_queue = deque()
        
    def queue_gesture(self, gesture: str, duration: float = 2.0):
        self.gesture_queue.append((gesture, time.time() + duration))
    
    def update(self, emotion: Emotion):
        current_time = time.time()
        
        # Check if current gesture expired
        if self.current_gesture != "idle" and current_time > self.gesture_timer:
            self.current_gesture = "idle"
        
        # Get new gesture from queue
        if not self.gesture_queue and self.current_gesture == "idle":
            # Auto gestures based on emotion
            if emotion == Emotion.HAPPY and random.random() > 0.98:
                self.queue_gesture("nod", 1.5)
            elif emotion == Emotion.ANALYZING and random.random() > 0.95:
                self.queue_gesture("think", 3.0)
        
        # Process queue
        while self.gesture_queue and current_time > self.gesture_queue[0][1]:
            self.gesture_queue.popleft()
        
        if self.gesture_queue and self.current_gesture == "idle":
            self.current_gesture, self.gesture_timer = self.gesture_queue[0]
    
    def render_gesture(self) -> str:
        if self.current_gesture == "nod":
            return '''
                <div style="animation: nod 1.5s ease-in-out infinite;">
                    <div style="font-size: 1.5rem;">👤</div>
                </div>
            '''
        elif self.current_gesture == "think":
            return '''
                <div style="animation: float 3s ease-in-out infinite;">
                    <div style="font-size: 1.5rem;">💭</div>
                </div>
            '''
        elif self.current_gesture == "point":
            return '''
                <div style="animation: point 2s ease-in-out infinite;">
                    <div style="font-size: 1.5rem;">☝️</div>
                </div>
            '''
        return '''
            <div style="animation: float 6s ease-in-out infinite;">
                <div style="font-size: 1.5rem;">🌀</div>
            </div>
        '''

# ==================== SISTEMA DE VOZ E ÁUDIO ====================
class AdvancedTTSService:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.is_muted = False
        self.volume = 0.9
        self.rate = 170
        self.pitch = 1.0
        self.emotion_modifiers = {
            Emotion.HAPPY: {"rate": 180, "pitch": 1.1, "volume": 0.95},
            Emotion.SAD: {"rate": 140, "pitch": 0.9, "volume": 0.8},
            Emotion.ANALYZING: {"rate": 160, "pitch": 1.0, "volume": 0.9},
            Emotion.DEFENSIVE: {"rate": 220, "pitch": 1.2, "volume": 1.0},
            Emotion.EXCITED: {"rate": 200, "pitch": 1.3, "volume": 0.98},
            Emotion.FOCUSED: {"rate": 155, "pitch": 1.05, "volume": 0.92},
            Emotion.SURPRISED: {"rate": 190, "pitch": 1.4, "volume": 0.96},
        }
        self._initialize_engine()
        self.audio_visualizer = AudioVisualizer()
    
    def _initialize_engine(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
        except Exception as e:
            st.warning(f"TTS não inicializado: {e}")
    
    def speak(self, text: str, emotion: Emotion = Emotion.NEUTRAL):
        if self.is_muted or not self.engine:
            return
        
        # Apply emotion modifiers
        modifiers = self.emotion_modifiers.get(emotion, {})
        rate = modifiers.get("rate", self.rate)
        pitch = modifiers.get("pitch", self.pitch)
        volume = modifiers.get("volume", self.volume)
        
        try:
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Simulate speaking animation
            self.is_speaking = True
            st.session_state.is_speaking = True
            self.audio_visualizer.start_speaking()
            
            # Start visualizer thread
            vis_thread = threading.Thread(
                target=self._run_visualizer_during_speech,
                args=(len(text.split()),),
                daemon=True
            )
            vis_thread.start()
            
            # Speak with emotion-based pauses
            words = text.split()
            for i, word in enumerate(words):
                if emotion in [Emotion.DEFENSIVE, Emotion.EXCITED] and random.random() > 0.8:
                    self.engine.setProperty('rate', rate + random.randint(-10, 10))
                
                self.engine.say(word + " ")
                
                # Add dramatic pauses
                if emotion == Emotion.ANALYZING and i % 5 == 4:
                    time.sleep(0.05)
                elif emotion == Emotion.DEFENSIVE and "!" in word:
                    time.sleep(0.1)
            
            self.engine.runAndWait()
            
        except Exception as e:
            st.error(f"Erro na fala: {e}")
        finally:
            self.is_speaking = False
            st.session_state.is_speaking = False
            self.audio_visualizer.stop_speaking()
    
    def _run_visualizer_during_speech(self, word_count: int):
        words_per_second = 3  # Average speaking rate
        duration = word_count / words_per_second
        
        start_time = time.time()
        while time.time() - start_time < duration and self.is_speaking:
            self.audio_visualizer.update()
            time.sleep(0.05)
    
    def stop(self):
        if self.engine:
            self.engine.stop()
        self.is_speaking = False
        st.session_state.is_speaking = False
        self.audio_visualizer.stop_speaking()

class AudioVisualizer:
    def __init__(self):
        self.is_active = False
        self.frequencies = deque([random.random() * 0.3 for _ in range(64)])
        self.smoothing_factor = 0.7
    
    def start_speaking(self):
        self.is_active = True
    
    def stop_speaking(self):
        self.is_active = False
    
    def update(self):
        if not self.is_active:
            # Gentle idle animation
            new_value = random.random() * 0.1
        else:
            # Active speaking animation
            base = random.random() * 0.8 + 0.2
            modulation = sin(time.time() * 20) * 0.3
            new_value = max(0, min(1, base + modulation))
        
        self.frequencies.append(new_value)
        if len(self.frequencies) > 64:
            self.frequencies.popleft()
    
    def get_bars(self, count: int = 20) -> List[float]:
        """Get audio bars for visualization"""
        if not self.frequencies:
            return [0.1] * count
        
        # Sample evenly from frequencies
        step = max(1, len(self.frequencies) // count)
        sampled = list(self.frequencies)[::step][:count]
        
        # Apply smoothing
        smoothed = []
        for i, val in enumerate(sampled):
            if i > 0:
                val = val * 0.3 + smoothed[-1] * 0.7
            smoothed.append(val)
        
        return smoothed

# ==================== SISTEMA DE MARKET DATA ====================
class MarketDataSystem:
    def __init__(self):
        self.prices = {
            "NASDAQ": deque([100 + random.random() * 10 for _ in range(100)], maxlen=100),
            "S&P500": deque([4500 + random.random() * 100 for _ in range(100)], maxlen=100),
            "DOW": deque([35000 + random.random() * 200 for _ in range(100)], maxlen=100),
            "BTC": deque([50000 + random.random() * 5000 for _ in range(100)], maxlen=100),
        }
        self.volumes = {k: deque([random.randint(1000, 10000) for _ in range(50)], maxlen=50) for k in self.prices.keys()}
        self.last_update = time.time()
        self.trends = {k: 0 for k in self.prices.keys()}  # -1 down, 0 neutral, 1 up
    
    def update(self):
        current_time = time.time()
        if current_time - self.last_update > 1:  # Update every second
            for symbol in self.prices.keys():
                # Generate realistic price movement
                last_price = self.prices[symbol][-1]
                movement = random.gauss(0, 0.5)  # Normal distribution
                if symbol == "BTC":
                    movement = random.gauss(0, 2)  # More volatile
                
                new_price = last_price + movement
                self.prices[symbol].append(new_price)
                
                # Update volume
                last_volume = self.volumes[symbol][-1]
                volume_change = random.randint(-500, 500)
                self.volumes[symbol].append(max(1000, last_volume + volume_change))
                
                # Calculate trend
                if len(self.prices[symbol]) > 10:
                    recent = list(self.prices[symbol])[-10:]
                    if recent[-1] > recent[0]:
                        self.trends[symbol] = 1
                    elif recent[-1] < recent[0]:
                        self.trends[symbol] = -1
                    else:
                        self.trends[symbol] = 0
            
            self.last_update = current_time
    
    def get_market_context(self) -> str:
        contexts = []
        for symbol, trend in self.trends.items():
            if trend == 1:
                contexts.append(f"{symbol} ↗")
            elif trend == -1:
                contexts.append(f"{symbol} ↘")
            else:
                contexts.append(f"{symbol} →")
        
        if sum(self.trends.values()) > 1:
            return f"Mercado em alta: {', '.join(contexts)}"
        elif sum(self.trends.values()) < -1:
            return f"Mercado em baixa: {', '.join(contexts)}"
        else:
            return f"Mercado misto: {', '.join(contexts[:3])}"
    
    def get_chart_html(self, symbol: str, width: int = 200, height: int = 60) -> str:
        if symbol not in self.prices:
            return ""
        
        prices = list(self.prices[symbol])
        if len(prices) < 2:
            return ""
        
        # Normalize prices for display
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price if max_price > min_price else 1
        
        # Create SVG path
        points = []
        for i, price in enumerate(prices):
            x = (i / (len(prices) - 1)) * width
            y = height - ((price - min_price) / price_range) * height * 0.8 - height * 0.1
            points.append(f"{x},{y}")
        
        path_data = f"M {' L '.join(points)}"
        
        # Determine color based on trend
        color = "#10b981" if self.trends[symbol] > 0 else "#ef4444" if self.trends[symbol] < 0 else "#6b7280"
        
        return f'''
            <svg width="{width}" height="{height}" style="border-radius: 4px; background: rgba(0,0,0,0.3);">
                <path d="{path_data}" stroke="{color}" stroke-width="2" fill="none" 
                      stroke-linecap="round" stroke-linejoin="round">
                    <animate attributeName="d" dur="1s" fill="freeze" 
                             to="{path_data}" repeatCount="1"/>
                </path>
                {f'<circle cx="{width}" cy="{points[-1].split(',')[1]}" r="3" fill="{color}"></circle>' if points else ''}
            </svg>
        '''

# ==================== AVATAR PRINCIPAL ====================
class AdvancedAvatarComponent:
    def __init__(self, market_context: str = None, broadcast: str = None):
        self.market_system = MarketDataSystem()
        self.particle_system = ParticleSystem()
        self.facial_animation = FacialAnimation()
        self.gesture_system = GestureSystem()
        self.tts_service = AdvancedTTSService()
        self.audio_visualizer = self.tts_service.audio_visualizer
        
        # Initialize session state
        self._init_session_state()
        
        # Auto-update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._auto_update, daemon=True)
        self.update_thread.start()
    
    def _init_session_state(self):
        defaults = {
            'avatar_visible': True,
            'avatar_expanded': False,
            'is_speaking': False,
            'is_muted': False,
            'is_thinking': False,
            'current_emotion': Emotion.NEUTRAL,
            'avatar_state': AvatarState.ACTIVE,
            'local_message': None,
            'chat_input': "",
            'show_speech': False,
            'particles_enabled': True,
            'animations_enabled': True,
            'chat_history': [],
            'market_data': {},
            'interaction_cooldown': 0,
            'last_interaction': time.time(),
            'health': 100,
            'energy': 100,
            'mood': 75,
            'notifications': [],
            'active_effects': [],
            'custom_theme': "dark",
            'voice_enabled': True,
            'auto_analyze': True,
            'alert_level': 0,
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def _auto_update(self):
        """Thread para atualizações automáticas"""
        while self.running:
            try:
                # Update market data
                self.market_system.update()
                
                # Update audio visualizer
                self.audio_visualizer.update()
                
                # Update particle system
                self.particle_system.update(0.033)
                
                # Auto-emotion based on market
                if st.session_state.auto_analyze and not st.session_state.is_speaking:
                    self._update_auto_emotion()
                
                # Energy and health management
                self._update_vitals()
                
                # Check for idle state
                if time.time() - st.session_state.last_interaction > 60:
                    if st.session_state.avatar_state != AvatarState.SLEEPING:
                        st.session_state.avatar_state = AvatarState.SLEEPING
                        st.session_state.current_emotion = Emotion.SLEEPING
                
                time.sleep(0.033)  # ~30 FPS
            except:
                time.sleep(1)
    
    def _update_auto_emotion(self):
        """Atualiza emoção automaticamente baseado no mercado"""
        market_trend = sum(self.market_system.trends.values())
        
        if market_trend >= 2:
            st.session_state.current_emotion = Emotion.HAPPY
        elif market_trend <= -2:
            st.session_state.current_emotion = Emotion.DEFENSIVE
        elif abs(market_trend) == 1:
            st.session_state.current_emotion = Emotion.FOCUSED
        elif random.random() > 0.99:
            st.session_state.current_emotion = random.choice([
                Emotion.CALM, Emotion.NEUTRAL, Emotion.FOCUSED
            ])
    
    def _update_vitals(self):
        """Atualiza saúde e energia do avatar"""
        # Energy drains when speaking/thinking
        if st.session_state.is_speaking:
            st.session_state.energy = max(0, st.session_state.energy - 0.1)
        elif st.session_state.is_thinking:
            st.session_state.energy = max(0, st.session_state.energy - 0.05)
        else:
            # Energy regenerates when idle
            st.session_state.energy = min(100, st.session_state.energy + 0.02)
        
        # Mood affects emotional responses
        if st.session_state.mood < 30:
            # More likely negative emotions
            if random.random() > 0.95:
                st.session_state.current_emotion = Emotion.SAD
    
    def analyze_emotion(self, text: str) -> Emotion:
        """Análise mais avançada de emoção"""
        if not text:
            return Emotion.NEUTRAL
        
        lower_text = text.lower()
        
        # Keywords for each emotion
        emotion_keywords = {
            Emotion.HAPPY: ['lucro', 'ganho', 'ótimo', 'excelente', 'positivo', 'alta', 'profit'],
            Emotion.EXCITED: ['oportunidade', 'chance', 'rápido', 'urgente', 'agora'],
            Emotion.SAD: ['perda', 'prejuízo', 'triste', 'queda', 'baixa', 'loss'],
            Emotion.DEFENSIVE: ['risco', 'perigo', 'stop', 'pânico', 'defesa', 'cuidado', 'alerta'],
            Emotion.ANALYZING: ['analisar', 'processar', 'varredura', 'scan', 'dados', 'estatística'],
            Emotion.FOCUSED: ['foco', 'atenção', 'importante', 'crucial', 'prioridade'],
            Emotion.SURPRISED: ['incrível', 'uau', 'surpresa', 'inesperado', '?', 'como'],
            Emotion.INTENSE: ['maximo', 'tudo', 'força total', 'máximo', '100%'],
        }
        
        # Check for emotion keywords
        emotion_scores = {emotion: 0 for emotion in emotion_keywords.keys()}
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in lower_text:
                    emotion_scores[emotion] += 1
        
        # Check for punctuation
        if '!' in text:
            if '!' * 3 in text:
                emotion_scores[Emotion.DEFENSIVE] += 2
            else:
                emotion_scores[Emotion.EXCITED] += 1
        
        if '?' in text:
            emotion_scores[Emotion.SURPRISED] += 1
        
        # Get highest scoring emotion
        max_score = max(emotion_scores.values())
        if max_score > 0:
            top_emotions = [e for e, s in emotion_scores.items() if s == max_score]
            return random.choice(top_emotions)
        
        return Emotion.NEUTRAL
    
    def display_message(self, message: str, emotion: Emotion = None, 
                       particle_effect: bool = True):
        """Exibe mensagem com efeitos visuais"""
        if not message:
            return
        
        if emotion is None:
            emotion = self.analyze_emotion(message)
        
        st.session_state.local_message = message
        st.session_state.current_emotion = emotion
        st.session_state.show_speech = True
        st.session_state.last_interaction = time.time()
        st.session_state.avatar_state = AvatarState.ACTIVE
        
        # Particle effect
        if particle_effect and st.session_state.particles_enabled:
            self._create_particle_effect(emotion)
        
        # Queue appropriate gesture
        if emotion == Emotion.HAPPY:
            self.gesture_system.queue_gesture("nod", 1.5)
        elif emotion == Emotion.ANALYZING:
            self.gesture_system.queue_gesture("think", 3.0)
        elif emotion == Emotion.DEFENSIVE:
            self.gesture_system.queue_gesture("point", 2.0)
        
        # TTS
        if st.session_state.voice_enabled and not st.session_state.is_muted:
            threading.Thread(
                target=self.tts_service.speak,
                args=(message, emotion),
                daemon=True
            ).start()
        
        # Auto-hide speech bubble
        def hide_speech():
            time.sleep(len(message) * 0.1 + 3)  # Dynamic timing based on message length
            st.session_state.show_speech = False
        
        threading.Thread(target=hide_speech, daemon=True).start()
    
    def _create_particle_effect(self, emotion: Emotion):
        """Cria efeito de partículas baseado na emoção"""
        symbols = ["•", "✦", "⭓", "⭔", "◈", "○", "□"]
        colors = {
            Emotion.HAPPY: ["#10b981", "#34d399", "#a7f3d0"],
            Emotion.DEFENSIVE: ["#ef4444", "#f87171", "#fca5a5"],
            Emotion.ANALYZING: ["#3b82f6", "#60a5fa", "#93c5fd"],
            Emotion.EXCITED: ["#f59e0b", "#fbbf24", "#fcd34d"],
            Emotion.SURPRISED: ["#f97316", "#fb923c", "#fdba74"],
        }
        
        particle_colors = colors.get(emotion, ["#06b6d4", "#22d3ee", "#67e8f9"])
        count = random.randint(15, 30)
        
        # Emit from center
        for _ in range(count):
            self.particle_system.emit(
                x=random.randint(100, 300),
                y=random.randint(100, 300),
                count=1,
                color=random.choice(particle_colors),
                symbol=random.choice(symbols),
                velocity_range=(-2, 2)
            )
    
    def send_chat_message(self):
        """Processa mensagem do chat"""
        message = st.session_state.chat_input.strip()
        if not message:
            return
        
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'text': message,
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'emotion': "user"
        })
        
        # Clear input
        st.session_state.chat_input = ""
        
        # Set thinking state
        st.session_state.is_thinking = True
        st.session_state.avatar_state = AvatarState.PROCESSING
        
        # Generate response
        response = self._generate_response(message)
        
        # Add AI response
        emotion = self.analyze_emotion(response)
        st.session_state.chat_history.append({
            'role': 'ai',
            'text': response,
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'emotion': emotion.emotion_name
        })
        
        # Display response
        st.session_state.is_thinking = False
        st.session_state.avatar_state = AvatarState.ACTIVE
        self.display_message(response, emotion)
        
        # Add notification
        self.add_notification("Resposta gerada", "💭")
    
    def _generate_response(self, message: str) -> str:
        """Gera resposta baseada no contexto"""
        # Simulate thinking delay
        time.sleep(max(0.5, min(2.0, len(message) * 0.05)))
        
        market_context = self.market_system.get_market_context()
        
        responses = {
            'greeting': [
                f"Link neural estabelecido. {market_context}",
                f"Conexão ativa. {market_context}",
                f"Sistema online. {market_context}"
            ],
            'analysis': [
                f"Analisando padrões de mercado... {market_context}",
                f"Processando dados em tempo real... {market_context}",
                f"Varredura profunda iniciada... {market_context}"
            ],
            'report': [
                f"Gerando relatório de mercado... {market_context}",
                f"Compilando dados para análise... {market_context}",
                f"Relatório de risco sendo processado... {market_context}"
            ],
            'panic': [
                f"🚨 PROTOCOLO DE DEFESA ATIVADO! {market_context}",
                f"⚠️ ALERTA DE RISCO ELEVADO! {market_context}",
                f"🔴 MODO DEFENSIVO ATIVADO! {market_context}"
            ],
            'default': [
                f"Processando comando... {market_context}",
                f"Entendido. {market_context}",
                f"Confirmado. {market_context}"
            ]
        }
        
        lower_msg = message.lower()
        
        if any(word in lower_msg for word in ['ola', 'oi', 'hello', 'hi']):
            return random.choice(responses['greeting'])
        elif any(word in lower_msg for word in ['analisar', 'analysis', 'scan']):
            return random.choice(responses['analysis'])
        elif any(word in lower_msg for word in ['relatorio', 'report', 'relatório']):
            return random.choice(responses['report'])
        elif any(word in lower_msg for word in ['panico', 'panic', 'defesa', 'defense']):
            return random.choice(responses['panic'])
        else:
            return random.choice(responses['default'])
    
    def quick_action(self, action: str):
        """Executa ação rápida"""
        actions = {
            'ANALYZE': {
                'message': "⚡ Iniciando varredura neural profunda dos mercados...",
                'emotion': Emotion.ANALYZING,
                'effect': 'analyze'
            },
            'REPORT': {
                'message': "📊 Gerando relatório de risco e oportunidade em tempo real...",
                'emotion': Emotion.FOCUSED,
                'effect': 'report'
            },
            'PANIC': {
                'message': "🛡️ ATIVANDO PROTOCOLO DE DEFESA! Cancelando ordens de risco...",
                'emotion': Emotion.DEFENSIVE,
                'effect': 'panic'
            },
            'CALM': {
                'message': "🌊 Ativando modo meditação. Estabilizando sistemas...",
                'emotion': Emotion.CALM,
                'effect': 'calm'
            },
            'ENERGY': {
                'message': "⚡ Recarregando sistemas. Níveis de energia sendo restaurados...",
                'emotion': Emotion.EXCITED,
                'effect': 'energy'
            }
        }
        
        if action in actions:
            action_data = actions[action]
            st.session_state.current_emotion = action_data['emotion']
            self.display_message(action_data['message'], action_data['emotion'])
            
            # Trigger external callback if exists
            if f'on_trigger_{action.lower()}' in st.session_state:
                st.session_state[f'on_trigger_{action.lower()}']()
    
    def add_notification(self, message: str, icon: str = "💡"):
        """Adiciona notificação"""
        st.session_state.notifications.append({
            'id': len(st.session_state.notifications),
            'message': message,
            'icon': icon,
            'time': datetime.now().strftime("%H:%M:%S"),
            'read': False
        })
    
    def render(self):
        """Renderiza o avatar completo"""
        self._render_styles()
        
        # Se avatar não está visível
        if not st.session_state.avatar_visible:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🌀 **SYLPH OFFLINE**", key="open_avatar", 
                           help="Clique para ativar o Assistente Sylph", 
                           use_container_width=True):
                    st.session_state.avatar_visible = True
                    st.rerun()
            return
        
        # Container principal
        expanded = st.session_state.avatar_expanded
        
        if expanded:
            self._render_expanded_view()
        else:
            self._render_compact_view()
    
    def _render_styles(self):
        """Renderiza todos os estilos CSS"""
        st.markdown("""
            <style>
            /* Animações principais */
            @keyframes pulse {
                0%, 100% { opacity: 0.3; transform: scale(1); }
                50% { opacity: 0.6; transform: scale(1.05); }
            }
            
            @keyframes glow {
                0% { opacity: 0.1; transform: scale(0.95); }
                100% { opacity: 0.4; transform: scale(1.05); }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            @keyframes nod {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                25% { transform: translateY(-5px) rotate(-5deg); }
                75% { transform: translateY(-5px) rotate(5deg); }
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-2px); }
                75% { transform: translateX(2px); }
            }
            
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @keyframes blink {
                0%, 100% { height: 8px; }
                50% { height: 2px; }
            }
            
            @keyframes wave {
                0%, 100% { transform: scaleY(0.3); }
                50% { transform: scaleY(1); }
            }
            
            /* Container do avatar */
            .avatar-container {
                position: fixed;
                bottom: 1rem;
                right: 1rem;
                z-index: 10000;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .avatar-main {
                background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(31, 41, 55, 0.95));
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 1rem;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.5),
                    0 0 0 1px rgba(255, 255, 255, 0.05),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                overflow: hidden;
                transition: all 0.3s ease;
            }
            
            .avatar-compact {
                width: 300px;
                height: 80px;
                border-radius: 40px;
                display: flex;
                align-items: center;
                padding: 0 1rem;
                cursor: pointer;
                position: relative;
            }
            
            .avatar-compact:hover {
                transform: translateY(-2px);
                box-shadow: 
                    0 25px 50px rgba(0, 0, 0, 0.6),
                    0 0 20px rgba(6, 182, 212, 0.3);
            }
            
            .avatar-expanded {
                width: 450px;
                height: 700px;
                display: flex;
                flex-direction: column;
            }
            
            /* Speech bubble */
            .speech-bubble {
                position: absolute;
                bottom: calc(100% + 0.5rem);
                right: 0;
                background: rgba(0, 0, 0, 0.9);
                border: 1px solid;
                border-radius: 1rem 1rem 0 1rem;
                backdrop-filter: blur(10px);
                padding: 1rem;
                max-width: 350px;
                font-size: 0.8rem;
                line-height: 1.4;
                animation: fadeInUp 0.3s ease-out;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                z-index: 10001;
            }
            
            .speech-bubble::after {
                content: '';
                position: absolute;
                bottom: -8px;
                right: 20px;
                border-width: 8px 8px 0;
                border-style: solid;
                border-color: rgba(0, 0, 0, 0.9) transparent transparent;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(10px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            /* Chat messages */
            .chat-message {
                padding: 0.75rem;
                border-radius: 1rem;
                margin-bottom: 0.75rem;
                max-width: 85%;
                font-size: 0.8rem;
                line-height: 1.4;
                position: relative;
                animation: slideIn 0.3s ease-out;
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateX(10px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            .user-message {
                background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(6, 182, 212, 0.1));
                border: 1px solid rgba(6, 182, 212, 0.3);
                margin-left: auto;
                border-top-right-radius: 0.25rem;
            }
            
            .ai-message {
                background: linear-gradient(135deg, rgba(55, 65, 81, 0.3), rgba(75, 85, 99, 0.2));
                border: 1px solid rgba(75, 85, 99, 0.3);
                margin-right: auto;
                border-top-left-radius: 0.25rem;
            }
            
            /* Quick actions */
            .quick-action-btn {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 0.75rem;
                border-radius: 0.75rem;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                cursor: pointer;
                transition: all 0.2s ease;
                min-width: 80px;
            }
            
            .quick-action-btn:hover {
                background: rgba(255, 255, 255, 0.1);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            }
            
            /* Health bars */
            .health-bar {
                height: 4px;
                border-radius: 2px;
                overflow: hidden;
                background: rgba(255, 255, 255, 0.1);
            }
            
            .health-fill {
                height: 100%;
                transition: width 0.3s ease;
            }
            
            /* Notifications */
            .notification {
                padding: 0.5rem 0.75rem;
                background: rgba(255, 255, 255, 0.05);
                border-left: 3px solid;
                border-radius: 0.25rem;
                margin-bottom: 0.5rem;
                font-size: 0.7rem;
                animation: slideInRight 0.3s ease-out;
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            /* Market charts */
            .market-chart {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 0.5rem;
                padding: 0.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Audio visualizer */
            .audio-visualizer {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 2px;
                height: 40px;
            }
            
            .audio-bar {
                width: 3px;
                border-radius: 1.5px;
                transition: height 0.1s ease;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def _render_compact_view(self):
        """Modo compacto do avatar"""
        emotion = st.session_state.current_emotion
        
        # Speech bubble
        if st.session_state.show_speech and st.session_state.local_message:
            st.markdown(f'''
                <div class="speech-bubble" style="border-color: {emotion.color};">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; 
                              color: {emotion.color}; font-size: 0.7rem; font-weight: bold;">
                        <span>📻</span> SYLPH • {emotion.emotion_name.upper()}
                    </div>
                    <div style="color: #e5e7eb;">
                        {st.session_state.local_message}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        
        # Container principal compacto
        st.markdown(f'''
            <div class="avatar-container">
                <div class="avatar-main avatar-compact" 
                     onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                     value: 'toggle_expand'}}, '*')">
                    
                    {/* Face e informações */}
                    <div style="display: flex; align-items: center; gap: 0.75rem; z-index: 10;">
                        {/* Face animada */}
                        {self.facial_animation.render_face(emotion)}
                        
                        {/* Informações de status */}
                        <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 0.75rem; font-weight: bold; color: white;">
                                    SYLPH AI
                                </span>
                                <span style="font-size: 0.6rem; color: {emotion.color}; 
                                          padding: 0.1rem 0.4rem; background: {emotion.color}22; 
                                          border-radius: 1rem;">
                                    {st.session_state.avatar_state.name}
                                </span>
                            </div>
                            
                            <div style="font-size: 0.6rem; color: #9ca3af;">
                                {self.market_system.get_market_context()}
                            </div>
                            
                            {/* Barras de status */}
                            <div style="display: flex; gap: 0.5rem; margin-top: 0.25rem;">
                                <div style="flex: 1;">
                                    <div class="health-bar">
                                        <div class="health-fill" style="width: {st.session_state.energy}%; 
                                             background: linear-gradient(90deg, #10b981, #34d399);"></div>
                                    </div>
                                    <div style="font-size: 0.5rem; color: #6b7280; text-align: center;">
                                        ENERGIA
                                    </div>
                                </div>
                                <div style="flex: 1;">
                                    <div class="health-bar">
                                        <div class="health-fill" style="width: {st.session_state.mood}%; 
                                             background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
                                    </div>
                                    <div style="font-size: 0.5rem; color: #6b7280; text-align: center;">
                                        HUMOR
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    {/* Controles rápidos */}
                    <div style="display: flex; gap: 0.5rem; margin-left: auto; z-index: 10;">
                        <button onclick="event.stopPropagation(); window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                               value: 'toggle_mute'}}, '*')" 
                               style="padding: 0.375rem; background: rgba(255, 255, 255, 0.1); 
                                      border: none; border-radius: 50%; cursor: pointer; 
                                      color: {'#ef4444' if st.session_state.is_muted else '#10b981'};">
                            <span style="font-size: 0.75rem;">{'🔇' if st.session_state.is_muted else '🔊'}</span>
                        </button>
                        
                        <button onclick="event.stopPropagation(); window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                               value: 'quick_action_ANALYZE'}}, '*')" 
                               style="padding: 0.375rem; background: rgba(59, 130, 246, 0.2); 
                                      border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 50%; 
                                      cursor: pointer; color: #3b82f6;">
                            <span style="font-size: 0.75rem;">⚡</span>
                        </button>
                    </div>
                    
                    {/* Partículas */}
                    <div style="position: absolute; inset: 0; pointer-events: none;">
                        {self.particle_system.render_html()}
                    </div>
                    
                    {/* Visualizador de áudio */}
                    {self._render_audio_visualizer(20, 30, emotion.color)}
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    def _render_expanded_view(self):
        """Modo expandido do avatar"""
        emotion = st.session_state.current_emotion
        
        st.markdown(f'''
            <div class="avatar-container">
                <div class="avatar-main avatar-expanded">
                    
                    {/* Header */}
                    <div style="display: flex; justify-content: space-between; align-items: center; 
                              padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); 
                              background: rgba(0, 0, 0, 0.3);">
                        
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            {self.facial_animation.render_face(emotion)}
                            
                            <div>
                                <div style="font-size: 0.9rem; font-weight: bold; color: white;">
                                    SYLPH ASSISTANT
                                </div>
                                <div style="font-size: 0.7rem; color: {emotion.color};">
                                    {emotion.emotion_name.upper()} • {st.session_state.avatar_state.name}
                                </div>
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 0.5rem;">
                            {self._render_control_buttons()}
                        </div>
                    </div>
                    
                    {/* Corpo principal */}
                    <div style="flex: 1; overflow: hidden; display: flex; flex-direction: column;">
                        
                        {/* Área de status */}
                        <div style="padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); 
                                  background: rgba(0, 0, 0, 0.2);">
                            {self._render_status_panel()}
                        </div>
                        
                        {/* Área de chat */}
                        <div style="flex: 1; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column;">
                            {self._render_chat_history()}
                            
                            {self._render_thinking_indicator()}
                        </div>
                        
                        {/* Input e ações */}
                        <div style="padding: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); 
                                  background: rgba(0, 0, 0, 0.3);">
                            {self._render_input_area()}
                            {self._render_quick_actions()}
                        </div>
                    </div>
                    
                    {/* Partículas no fundo */}
                    <div style="position: absolute; inset: 0; pointer-events: none; z-index: -1;">
                        {self.particle_system.render_html()}
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    def _render_control_buttons(self) -> str:
        """Renderiza botões de controle"""
        return f'''
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                   value: 'toggle_mute'}}, '*')" 
                   style="padding: 0.375rem; background: rgba(255, 255, 255, 0.1); 
                          border: none; border-radius: 50%; cursor: pointer; 
                          color: {'#ef4444' if st.session_state.is_muted else '#10b981'}; 
                          transition: all 0.2s;">
                <span style="font-size: 0.75rem;">{'🔇' if st.session_state.is_muted else '🔊'}</span>
            </button>
            
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                   value: 'toggle_expand'}}, '*')" 
                   style="padding: 0.375rem; background: rgba(255, 255, 255, 0.1); 
                          border: none; border-radius: 50%; cursor: pointer; 
                          color: #f59e0b; transition: all 0.2s;">
                <span style="font-size: 0.75rem;">🗕</span>
            </button>
            
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                   value: 'close_avatar'}}, '*')" 
                   style="padding: 0.375rem; background: rgba(239, 68, 68, 0.2); 
                          border: none; border-radius: 50%; cursor: pointer; 
                          color: #ef4444; transition: all 0.2s;">
                <span style="font-size: 0.75rem;">✕</span>
            </button>
        '''
    
    def _render_status_panel(self) -> str:
        """Renderiza painel de status"""
        return f'''
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                
                {/* Status do avatar */}
                <div>
                    <div style="font-size: 0.7rem; color: #6b7280; margin-bottom: 0.5rem;">
                        STATUS DO SISTEMA
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <div>
                            <div style="display: flex; justify-content: space-between; 
                                      font-size: 0.7rem; color: #9ca3af; margin-bottom: 0.25rem;">
                                <span>ENERGIA</span>
                                <span>{st.session_state.energy:.0f}%</span>
                            </div>
                            <div class="health-bar">
                                <div class="health-fill" style="width: {st.session_state.energy}%; 
                                     background: linear-gradient(90deg, #10b981, #34d399);"></div>
                            </div>
                        </div>
                        
                        <div>
                            <div style="display: flex; justify-content: space-between; 
                                      font-size: 0.7rem; color: #9ca3af; margin-bottom: 0.25rem;">
                                <span>HUMOR</span>
                                <span>{st.session_state.mood:.0f}%</span>
                            </div>
                            <div class="health-bar">
                                <div class="health-fill" style="width: {st.session_state.mood}%; 
                                     background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                {/* Dados do mercado */}
                <div>
                    <div style="font-size: 0.7rem; color: #6b7280; margin-bottom: 0.5rem;">
                        MERCADO EM TEMPO REAL
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                        {self._render_market_charts()}
                    </div>
                </div>
            </div>
        '''
    
    def _render_market_charts(self) -> str:
        """Renderiza gráficos do mercado"""
        charts_html = ""
        for symbol in ["NASDAQ", "S&P500", "BTC"]:
            chart = self.market_system.get_chart_html(symbol, width=150, height=40)
            trend = self.market_system.trends[symbol]
            trend_icon = "↗" if trend > 0 else "↘" if trend < 0 else "→"
            trend_color = "#10b981" if trend > 0 else "#ef4444" if trend < 0 else "#6b7280"
            
            charts_html += f'''
                <div>
                    <div style="display: flex; justify-content: space-between; 
                              align-items: center; margin-bottom: 0.25rem;">
                        <span style="font-size: 0.7rem; color: #9ca3af;">{symbol}</span>
                        <span style="font-size: 0.7rem; color: {trend_color}; 
                                  font-weight: bold;">{trend_icon}</span>
                    </div>
                    {chart}
                </div>
            '''
        
        return charts_html
    
    def _render_chat_history(self) -> str:
        """Renderiza histórico do chat"""
        if not st.session_state.chat_history:
            return '''
                <div style="text-align: center; color: #6b7280; padding: 2rem;">
                    <div style="font-size: 2rem; margin-bottom: 1rem; opacity: 0.5;">🌀</div>
                    <div style="font-size: 0.8rem; margin-bottom: 0.5rem;">
                        Link Neural Estabelecido
                    </div>
                    <div style="font-size: 0.7rem; opacity: 0.7;">
                        Aguardando comando de voz ou texto
                    </div>
                </div>
            '''
        
        chat_html = ""
        for msg in st.session_state.chat_history[-20:]:
            if msg['role'] == 'user':
                chat_html += f'''
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 0.75rem;">
                        <div class="chat-message user-message">
                            {msg['text']}
                            <div style="font-size: 0.6rem; color: rgba(255, 255, 255, 0.5); 
                                      margin-top: 0.25rem; text-align: right;">
                                {msg['timestamp']}
                            </div>
                        </div>
                    </div>
                '''
            else:
                emotion_color = ""
                for emotion in Emotion:
                    if emotion.emotion_name == msg.get('emotion', ''):
                        emotion_color = emotion.color
                        break
                
                chat_html += f'''
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 0.75rem;">
                        <div class="chat-message ai-message">
                            <div style="display: flex; align-items: center; gap: 0.5rem; 
                                      margin-bottom: 0.25rem;">
                                <span style="font-size: 0.7rem; color: {emotion_color}; 
                                          font-weight: bold;">
                                    {msg.get('emotion', 'ai').upper()}
                                </span>
                            </div>
                            {msg['text']}
                            <div style="font-size: 0.6rem; color: rgba(209, 213, 219, 0.5); 
                                      margin-top: 0.25rem;">
                                {msg['timestamp']}
                            </div>
                        </div>
                    </div>
                '''
        
        return chat_html
    
    def _render_thinking_indicator(self) -> str:
        """Renderiza indicador de pensamento"""
        if not st.session_state.is_thinking:
            return ""
        
        return '''
            <div style="display: flex; justify-content: flex-start; margin-bottom: 0.75rem;">
                <div class="chat-message ai-message">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div class="thinking-dots">
                            <div class="thinking-dot"></div>
                            <div class="thinking-dot"></div>
                            <div class="thinking-dot"></div>
                        </div>
                        <span style="font-size: 0.7rem; color: #6b7280;">
                            Processando...
                        </span>
                    </div>
                </div>
            </div>
        '''
    
    def _render_input_area(self) -> str:
        """Renderiza área de input"""
        return f'''
            <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                <div style="flex: 1; position: relative;">
                    <input type="text" id="chat_input" 
                           style="width: 100%; padding: 0.75rem; padding-right: 2.5rem;
                                  background: rgba(255, 255, 255, 0.05); 
                                  border: 1px solid rgba(255, 255, 255, 0.1);
                                  border-radius: 0.75rem; color: white;
                                  font-size: 0.8rem; outline: none;"
                           placeholder="Digite seu comando neural..."
                           onkeypress="if(event.keyCode==13) window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                                   value: 'send_message'}}, '*')">
                    <span style="position: absolute; right: 0.75rem; top: 50%; 
                              transform: translateY(-50%); font-size: 0.8rem; color: #6b7280; 
                              cursor: pointer;" 
                          onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                                  value: 'start_voice'}}, '*')">
                        🎤
                    </span>
                </div>
                <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                       value: 'send_message'}}, '*')"
                       style="padding: 0.75rem; background: linear-gradient(135deg, #06b6d4, #0ea5e9); 
                              border: none; border-radius: 0.75rem; cursor: pointer; 
                              transition: all 0.2s;">
                    <span style="font-size: 0.8rem; color: white;">📤</span>
                </button>
            </div>
        '''
    
    def _render_quick_actions(self) -> str:
        """Renderiza ações rápidas"""
        actions = [
            ("ANALYZE", "⚡", "Análise Rápida", "#3b82f6"),
            ("REPORT", "📊", "Relatório", "#8b5cf6"),
            ("PANIC", "🛡️", "Defesa", "#ef4444"),
            ("CALM", "🌊", "Calmaria", "#14b8a6"),
            ("ENERGY", "🔋", "Energia", "#f59e0b"),
            ("SETTINGS", "⚙️", "Config", "#6b7280"),
        ]
        
        actions_html = '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">'
        
        for action, icon, label, color in actions:
            actions_html += f'''
                <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                       value: 'quick_action_{action}'}}, '*')"
                       class="quick-action-btn">
                    <span style="font-size: 1rem; color: {color};">{icon}</span>
                    <span style="font-size: 0.6rem; color: #9ca3af; margin-top: 0.25rem;">
                        {label}
                    </span>
                </button>
            '''
        
        actions_html += '</div>'
        return actions_html
    
    def _render_audio_visualizer(self, bar_count: int = 20, max_height: int = 40, color: str = "#06b6d4") -> str:
        """Renderiza visualizador de áudio"""
        bars = self.audio_visualizer.get_bars(bar_count)
        
        bars_html = ""
        for i, height in enumerate(bars):
            bar_height = max(4, height * max_height)
            delay = i * 0.05
            bars_html += f'''
                <div class="audio-bar" style="height: {bar_height}px; 
                      background: linear-gradient(to top, {color}, {color}88);
                      animation: wave 0.5s ease-in-out infinite alternate;
                      animation-delay: {delay}s;"></div>
            '''
        
        return f'''
            <div class="audio-visualizer" style="position: absolute; inset: 0; 
                  opacity: {0.3 + 0.7 * st.session_state.is_speaking}; 
                  transition: opacity 0.3s ease;">
                {bars_html}
            </div>
        '''

# ==================== APLICAÇÃO PRINCIPAL ====================
def main():
    st.set_page_config(
        page_title="SYLPH AI Assistant",
        page_icon="🌀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Hide Streamlit default elements
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {background: transparent;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Initialize avatar
    if 'avatar' not in st.session_state:
        st.session_state.avatar = AdvancedAvatarComponent()
    
    avatar = st.session_state.avatar
    
    # Setup callbacks
    callbacks = {
        'on_trigger_analyze': lambda: (
            st.toast("🔍 Análise profunda iniciada!", icon="⚡"),
            avatar.add_notification("Análise de mercado em andamento", "📈")
        ),
        'on_trigger_panic': lambda: (
            st.toast("🚨 Protocolo de defesa ativado!", icon="⚠️"),
            avatar.add_notification("Sistema em modo defensivo", "🛡️")
        ),
        'on_trigger_report': lambda: (
            st.toast("📊 Gerando relatório...", icon="📈"),
            avatar.add_notification("Relatório sendo compilado", "📄")
        ),
    }
    
    for key, callback in callbacks.items():
        if key not in st.session_state:
            st.session_state[key] = callback
    
    # Handle JavaScript events
    if 'js_event' in st.session_state:
        event = st.session_state.js_event
        
        if event == 'toggle_mute':
            avatar.tts_service.is_muted = not avatar.tts_service.is_muted
            st.session_state.is_muted = avatar.tts_service.is_muted
            avatar.add_notification(
                "Áudio " + ("silenciado" if avatar.tts_service.is_muted else "ativado"),
                "🔇" if avatar.tts_service.is_muted else "🔊"
            )
        
        elif event == 'toggle_expand':
            st.session_state.avatar_expanded = not st.session_state.avatar_expanded
        
        elif event == 'close_avatar':
            st.session_state.avatar_visible = False
        
        elif event.startswith('quick_action_'):
            action = event.replace('quick_action_', '')
            avatar.quick_action(action)
        
        elif event == 'send_message':
            avatar.send_chat_message()
        
        elif event == 'start_voice':
            avatar.display_message("Modo voz ativado. Falando...", Emotion.FOCUSED)
        
        st.session_state.js_event = ''
        st.rerun()
    
    # JavaScript listener
    st.markdown("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:setComponentValue') {
                Streamlit.setComponentValue(event.data.value);
            }
        });
        
        // Handle button clicks
        document.addEventListener('click', function(e) {
            if (e.target.closest('button')) {
                const btn = e.target.closest('button');
                if (btn.onclick && btn.onclick.toString().includes('postMessage')) {
                    // Let the onclick handler run
                    return;
                }
                
                // Check for data-action attribute
                const action = btn.getAttribute('data-action');
                if (action) {
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: action
                    }, '*');
                }
            }
        });
        </script>
    """, unsafe_allow_html=True)
    
    # Main content
    st.markdown("""
        <div style="min-height: 100vh; background: linear-gradient(135deg, #0f172a, #1e293b); 
                  position: fixed; inset: 0; z-index: -1;"></div>
    """, unsafe_allow_html=True)
    
    # Dashboard content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem;">
                <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem;">
                    <span style="color: #06b6d4;">SYLPH</span> AI
                </h1>
                <p style="color: #94a3b8; font-size: 1.1rem;">
                    Assistente Neural para Análise de Mercados
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Market dashboard
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.5); border-radius: 1rem; 
                      padding: 1.5rem; margin-bottom: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h3 style="color: white; margin-bottom: 1rem;">📈 Dashboard de Mercado</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 0.5rem;">
                        <div style="color: #94a3b8; font-size: 0.9rem;">NASDAQ</div>
                        <div style="color: #10b981; font-size: 1.5rem; font-weight: bold;">
                            {:.2f} ↗
                        </div>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 0.5rem;">
                        <div style="color: #94a3b8; font-size: 0.9rem;">S&P500</div>
                        <div style="color: #ef4444; font-size: 1.5rem; font-weight: bold;">
                            {:.2f} ↘
                        </div>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 0.5rem;">
                        <div style="color: #94a3b8; font-size: 0.9rem;">BTC</div>
                        <div style="color: #f59e0b; font-size: 1.5rem; font-weight: bold;">
                            {:.0f} ↗
                        </div>
                    </div>
                </div>
            </div>
        """.format(
            random.uniform(15000, 17000),
            random.uniform(4500, 5000),
            random.uniform(50000, 60000)
        ), unsafe_allow_html=True)
    
    # Render avatar
    avatar.render()
    
    # Auto-refresh
    time.sleep(0.1)
    st.rerun()

if __name__ == "__main__":
    main()