import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'package:frontend/routes.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final usernameController = TextEditingController();
  final passwordController = TextEditingController();
  String error = '';

  void loginUser() async {
    final response = await AuthService.login(
      usernameController.text,
      passwordController.text,
    );

    if (response.statusCode == 200) {
      // handle success (e.g., save token, navigate)
      Navigator.pushReplacementNamed(context, Routes.home);
    } else {
      setState(() {
        error = 'Login failed. Check your credentials.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: usernameController,
              decoration: const InputDecoration(labelText: 'Username'),
            ),
            TextField(
              controller: passwordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Password'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: loginUser, child: const Text('Login')),
            Text(error, style: const TextStyle(color: Colors.red)),
            TextButton(
              onPressed: () => Navigator.pushNamed(context, Routes.register),
              child: const Text("Don't have an account? Register"),
            ),
          ],
        ),
      ),
    );
  }
}
