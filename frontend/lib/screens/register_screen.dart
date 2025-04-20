import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'package:image_picker/image_picker.dart';
import 'package:frontend/routes.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final usernameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final firstNameController = TextEditingController();
  final lastNameController = TextEditingController();
  File? _image;

  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage() async {
    final picked = await _picker.pickImage(source: ImageSource.gallery);
    if (picked != null) {
      setState(() {
        _image = File(picked.path);
      });
    }
  }

  String error = '';

  Future<void> registerUser() async {
    final response = await AuthService.register(
      usernameController.text,
      emailController.text,
      passwordController.text,
      firstNameController.text,
      lastNameController.text,
      _image,
    );
    // print("Status code: ${response.statusCode}");
    // print("Body: ${response.body}");
    if (response.statusCode == 201) {
      // Success! Navigate to login
      Navigator.pushReplacementNamed(context, Routes.login);
    } else {
      final responseData = jsonDecode(response.body);
      String errormsg = _getErrorMessage(responseData);
      setState(() {
        error = 'Registration failed: $errormsg';
      });
    }
  }

  String _getErrorMessage(Map<String, dynamic> responseData) {
    // Check if the error is related to the email field
    if (responseData.containsKey('email')) {
      return responseData['email'][0]; // Return the first error for the email field
    }
    // Check if the error is related to the username field
    if (responseData.containsKey('username')) {
      return responseData['username'][0]; // Return the first error for the username field
    }
    // Check if the error is related to the password field
    if (responseData.containsKey('password')) {
      return responseData['password'][0]; // Return the first error for the password field
    }

    // If no specific error, return a generic message
    return 'An error occurred. Please try again.';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const SizedBox(height: 12),
            TextButton.icon(
              onPressed: _pickImage,
              icon: Icon(Icons.image),
              label: Text('Pick Profile Picture'),
            ),
            if (_image != null)
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Image.file(_image!, height: 100),
              ),
            TextField(
              controller: usernameController,
              decoration: const InputDecoration(labelText: 'Username'),
            ),
            TextField(
              controller: emailController,
              decoration: const InputDecoration(labelText: 'Email'),
            ),
            TextField(
              controller: passwordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Password'),
            ),
            TextFormField(
              controller: firstNameController,
              decoration: InputDecoration(labelText: 'First Name'),
            ),

            TextFormField(
              controller: lastNameController,
              decoration: InputDecoration(labelText: 'Last Name'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: registerUser,
              child: const Text('Register'),
            ),
            Text(error, style: const TextStyle(color: Colors.red)),
            TextButton(
              onPressed: () => Navigator.pushNamed(context, Routes.login),
              child: const Text('Already have an account? Login'),
            ),
          ],
        ),
      ),
    );
  }
}
