import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function TasksScreen() {
  const [tasks, setTasks] = useState<any[]>([]);

  useEffect(() => {
    apiGet('/api/tasks').then(setTasks).catch(() => setTasks([]));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Tasks</Text>
      {tasks.map((task) => (
        <View key={task.id} style={styles.card}>
          <Text style={styles.taskTitle}>{task.title}</Text>
          <Text style={styles.text}>{task.description || 'No description provided.'}</Text>
          <Text style={styles.meta}>Status: {task.status} • Assignee: {task.assignee}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: 20 },
  title: { fontSize: 28, color: theme.colors.text, marginBottom: 16 },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  taskTitle: { color: theme.colors.text, fontSize: 18, fontWeight: '700', marginBottom: 6 },
  text: { color: theme.colors.text },
  meta: { color: theme.colors.muted, marginTop: 8 },
});
