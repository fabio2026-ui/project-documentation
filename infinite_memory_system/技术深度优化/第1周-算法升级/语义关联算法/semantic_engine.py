#!/usr/bin/env python3
"""
语义关联引擎 - 基于Transformer的语义分析系统
实现文本向量化、相似度计算和智能关联发现
"""

import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
import logging
from dataclasses import dataclass
from datetime import datetime

# 导入语义模型
try:
    from sentence_transformers import SentenceTransformer
    import torch
    SEMANTIC_MODEL_AVAILABLE = True
except ImportError:
    SEMANTIC_MODEL_AVAILABLE = False
    print("警告: sentence-transformers 未安装，使用简单文本匹配")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SemanticResult:
    """语义分析结果"""
    text: str
    vector: np.ndarray
    language: str
    keywords: List[str]
    entities: List[str]
    sentiment: float  # -1到1，负数为负面，正数为正面
    confidence: float  # 分析置信度


class SemanticEngine:
    """语义分析引擎"""
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2',
                 cache_dir: str = '/tmp/semantic_cache'):
        """
        初始化语义引擎
        
        Args:
            model_name: 语义模型名称
            cache_dir: 缓存目录
        """
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.model = None
        self.cache = {}
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'inference_time': 0,
            'last_loaded': None
        }
        
        # 创建缓存目录
        os.makedirs(cache_dir, exist_ok=True)
        
        # 加载模型
        self._load_model()
        
        # 语言检测关键词
        self.language_keywords = {
            'zh': ['的', '是', '在', '和', '有', '了', '我', '你', '他', '她'],
            'en': ['the', 'is', 'in', 'and', 'to', 'of', 'a', 'for', 'that', 'with'],
            'it': ['il', 'la', 'e', 'di', 'che', 'per', 'con', 'su', 'da', 'in']
        }
    
    def _load_model(self):
        """加载语义模型"""
        if not SEMANTIC_MODEL_AVAILABLE:
            logger.warning("sentence-transformers 不可用，使用简单文本匹配模式")
            return
        
        try:
            logger.info(f"正在加载语义模型: {self.model_name}")
            start_time = datetime.now()
            
            # 使用缓存加载模型
            cache_path = os.path.join(self.cache_dir, f"{self.model_name.replace('/', '_')}.cache")
            
            if os.path.exists(cache_path):
                logger.info(f"从缓存加载模型: {cache_path}")
                self.model = SentenceTransformer(cache_path)
            else:
                logger.info(f"下载并缓存模型: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                self.model.save(cache_path)
            
            load_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"模型加载完成，耗时: {load_time:.2f}秒")
            
            # 测试模型
            test_text = "这是一个测试文本"
            test_vector = self.model.encode(test_text)
            logger.info(f"模型测试成功，向量维度: {test_vector.shape}")
            
            self.stats['last_loaded'] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            self.model = None
    
    def analyze_text(self, text: str, use_cache: bool = True) -> Optional[SemanticResult]:
        """
        分析文本语义
        
        Args:
            text: 输入文本
            use_cache: 是否使用缓存
            
        Returns:
            SemanticResult 或 None
        """
        self.stats['total_requests'] += 1
        
        # 检查缓存
        cache_key = f"analyze_{hash(text)}"
        if use_cache and cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]
        
        try:
            # 文本预处理
            cleaned_text = self._preprocess_text(text)
            
            # 语言检测
            language = self._detect_language(cleaned_text)
            
            # 向量化
            vector = self._get_text_vector(cleaned_text)
            
            # 关键词提取
            keywords = self._extract_keywords(cleaned_text, language)
            
            # 实体识别（简化版）
            entities = self._extract_entities(cleaned_text, language)
            
            # 情感分析（简化版）
            sentiment = self._analyze_sentiment(cleaned_text, language)
            
            # 构建结果
            result = SemanticResult(
                text=cleaned_text,
                vector=vector,
                language=language,
                keywords=keywords,
                entities=entities,
                sentiment=sentiment,
                confidence=0.8  # 默认置信度
            )
            
            # 缓存结果
            if use_cache:
                self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"文本分析失败: {e}")
            return None
    
    def _preprocess_text(self, text: str) -> str:
        """文本预处理"""
        # 去除多余空格和换行
        cleaned = ' '.join(text.strip().split())
        
        # 限制长度（避免过长文本）
        max_length = 1000
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length] + "..."
        
        return cleaned
    
    def _detect_language(self, text: str) -> str:
        """检测文本语言"""
        text_lower = text.lower()
        
        # 统计关键词出现次数
        scores = {}
        for lang, keywords in self.language_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[lang] = score
        
        # 返回得分最高的语言
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return 'unknown'
    
    def _get_text_vector(self, text: str) -> np.ndarray:
        """获取文本向量"""
        if self.model is not None:
            # 使用语义模型
            vector = self.model.encode(text)
            return vector
        else:
            # 回退方案：使用词频向量
            words = text.lower().split()
            unique_words = list(set(words))
            vector = np.zeros(len(unique_words))
            
            for i, word in enumerate(unique_words):
                vector[i] = words.count(word) / len(words)
            
            return vector
    
    def _extract_keywords(self, text: str, language: str) -> List[str]:
        """提取关键词（简化版）"""
        words = text.lower().split()
        
        # 过滤停用词
        stop_words = self._get_stop_words(language)
        filtered_words = [w for w in words if w not in stop_words and len(w) > 1]
        
        # 统计词频
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 返回频率最高的5个词
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        return [word for word, freq in top_words]
    
    def _get_stop_words(self, language: str) -> set:
        """获取停用词列表"""
        stop_words = {
            'zh': {'的', '是', '在', '和', '有', '了', '我', '你', '他', '她', '它', '这', '那'},
            'en': {'the', 'is', 'in', 'and', 'to', 'of', 'a', 'for', 'that', 'with', 'on', 'at'},
            'it': {'il', 'la', 'e', 'di', 'che', 'per', 'con', 'su', 'da', 'in', 'un', 'una'},
            'default': {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        }
        
        return stop_words.get(language, stop_words['default'])
    
    def _extract_entities(self, text: str, language: str) -> List[str]:
        """提取实体（简化版）"""
        # 这里实现一个简单的实体识别
        # 实际应用中应该使用NER模型
        entities = []
        
        # 识别大写单词（可能为专有名词）
        words = text.split()
        for word in words:
            if word.istitle() and len(word) > 2:
                entities.append(word)
        
        return list(set(entities))[:5]  # 去重并限制数量
    
    def _analyze_sentiment(self, text: str, language: str) -> float:
        """情感分析（简化版）"""
        # 简单关键词匹配
        positive_words = {
            'zh': {'好', '优秀', '成功', '快乐', '喜欢', '爱', '满意', '高兴', '完美', '棒'},
            'en': {'good', 'great', 'excellent', 'happy', 'love', 'like', 'perfect', 'awesome', 'best', 'nice'},
            'it': {'buono', 'ottimo', 'eccellente', 'felice', 'amore', 'perfetto', 'fantastico', 'bello', 'bravo'}
        }
        
        negative_words = {
            'zh': {'坏', '糟糕', '失败', '悲伤', '讨厌', '恨', '不满意', '生气', '差', '烂'},
            'en': {'bad', 'terrible', 'awful', 'sad', 'hate', 'dislike', 'angry', 'poor', 'worst', 'horrible'},
            'it': {'cattivo', 'terribile', 'orribile', 'triste', 'odio', 'arrabbiato', 'pessimo', 'brutto', 'male'}
        }
        
        text_lower = text.lower()
        pos_words = positive_words.get(language, positive_words['en'])
        neg_words = negative_words.get(language, negative_words['en'])
        
        pos_count = sum(1 for word in pos_words if word in text_lower)
        neg_count = sum(1 for word in neg_words if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0
        
        # 计算情感分数（-1到1）
        sentiment = (pos_count - neg_count) / total
        return max(-1.0, min(1.0, sentiment))
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的语义相似度
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            相似度分数（0到1）
        """
        # 分析两个文本
        result1 = self.analyze_text(text1)
        result2 = self.analyze_text(text2)
        
        if result1 is None or result2 is None:
            return 0.0
        
        # 计算向量相似度（余弦相似度）
        vector1 = result1.vector
        vector2 = result2.vector
        
        # 确保向量维度一致
        if len(vector1) != len(vector2):
            min_len = min(len(vector1), len(vector2))
            vector1 = vector1[:min_len]
            vector2 = vector2[:min_len]
        
        # 计算余弦相似度
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # 确保在0-1范围内
        similarity = max(0.0, min(1.0, similarity))
        
        return similarity
    
    def find_similar_texts(self, query_text: str, texts: List[str], 
                          threshold: float = 0.5, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        在文本列表中查找相似的文本
        
        Args:
            query_text: 查询文本
            texts: 文本列表
            threshold: 相似度阈值
            top_k: 返回最多结果数
            
        Returns:
            列表[(文本, 相似度), ...]
        """
        similarities = []
        
        # 分析查询文本
        query_result = self.analyze_text(query_text)
        if query_result is None:
            return []
        
        query_vector = query_result.vector
        
        for text in texts:
            # 分析目标文本
            text_result = self.analyze_text(text)
            if text_result is None:
                continue
            
            # 计算相似度
            similarity = self.calculate_similarity(query_text, text)
            
            if similarity >= threshold:
                similarities.append((text, similarity))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def batch_analyze(self, texts: List[str]) -> List[Optional[SemanticResult]]:
        """批量分析文本"""
        results = []
        for text in texts:
            result = self.analyze_text(text)
            results.append(result)
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息"""
        return {
            'model_name': self.model_name,
            'model_loaded': self.model is not None,
            'cache_size': len(self.cache),
            'stats': self.stats,
            'cache_dir': self.cache_dir
        }
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        logger.info("语义引擎缓存已清空")
    
    def save_cache(self, filepath: str):
        """保存缓存到文件"""
        try:
            # 转换缓存数据为可序列化格式
            cache_data = {}
            for key, result in self.cache.items():
                cache_data[key] = {
                    'text': result.text,
                    'vector': result.vector.tolist(),
                    'language': result.language,
                    'keywords': result.keywords,
                    'entities': result.entities,
                    'sentiment': result.sentiment,
                    'confidence': result.confidence
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"缓存已保存到: {filepath}")
            
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")
    
    def load_cache(self, filepath: str):
        """从文件加载缓存"""
        try:
            if not os.path.exists(filepath):
                logger.warning(f"缓存文件不存在: {filepath}")
                return
            
            with open(filepath, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # 转换回SemanticResult对象
            for key, data in cache_data.items():
                result = SemanticResult(
                    text=data['text'],
                    vector=np.array(data['vector']),
                    language=data['language'],
                    keywords=data['keywords'],
                    entities=data['entities'],
                    sentiment=data['sentiment'],
                    confidence=data['confidence']
                )
                self.cache[key] = result
            
            logger.info(f"缓存已从文件加载: {filepath}")
            
        except Exception as e:
            logger.error(f"加载缓存失败: {e}")


# 测试函数
def test_semantic_engine():
    """测试语义引擎"""
    print("🧠 测试语义引擎...")
    
    # 创建引擎
    engine = SemanticEngine()
    
    # 测试文本
    texts = [
        "Python是一种高级编程语言，简洁易读",
        "机器学习是人工智能的重要分支",
        "今天天气很好，阳光明媚",
        "这个产品非常糟糕，质量很差"
    ]
    
    # 测试单个文本分析
    print("\n📝 测试文本分析:")
    for text in texts:
        result = engine.analyze_text(text)
        if result:
            print(f"\n文本: {text[:30]}...")
            print(f"语言: {result.language}")
            print(f"关键词: {result.keywords}")
            print(f"情感: {result.sentiment:.2f}")
            print(f"向量维度: {result.vector.shape}")
    
    # 测试相似度计算
    print("\n🔗 测试相似度计算:")
    text1 = "Python编程语言"
    text2 = "机器学习算法"
    text3 = "Java编程语言"
    
    sim12 = engine.calculate_similarity(text1, text2)
    sim13 = engine.calculate_similarity(text1, text3)
    
    print(f"'{text1}' 与 '{text2}' 相似度: {sim12:.3f}")
    print(f"'{text1}' 与 '{text3}' 相似度: {sim13:.3f}")
    
    # 测试批量查找
    print("\n🔍 测试相似文本查找:")
    query = "编程语言学习"
    similar = engine.find_similar_texts(query, texts, threshold=0.3)
    
    print(f"查询: '{query}'")
    for text, similarity in similar:
        print(f"  相似度 {similarity:.3f}: {text[:40]}...")
    
    # 显示统计信息
    print("\n📊 引擎统计:")
    stats = engine.get_stats()
    for key, value in stats.items():
        if key == 'stats':
            print(f"  详细统计:")
            for stat_key, stat_value in value.items():
                print(f"    {stat_key}: {stat_value}")
        else:
            print(f"  {key}: {value}")
    
    print("\n✅ 语义引擎测试完成！")


if __name__ == "__main__":
    test_semantic_engine()