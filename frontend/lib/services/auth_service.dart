import 'dart:convert';
// import 'dart:developer';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  static const String baseUrl = 'http://127.0.0.1:8000/api'; // testing url

  static Future<http.Response> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login/'),
      body: {'username': username, 'password': password},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', data['token']);
      await prefs.setBool('is_staff', data['is_staff']);
      await prefs.setString('username', data['username']);
    }

    return response;
  }

  static Future<http.Response> register(
    String username,
    String email,
    String password,
    String firstname,
    String lastname, [
    File? image, //optional
    bool isAdmin = false,
  ]) async {
    var uri = Uri.parse('$baseUrl/register/');
    var request = http.MultipartRequest('POST', uri);

    request.fields['username'] = username;
    request.fields['email'] = email;
    request.fields['password'] = password;
    request.fields['first_name'] = firstname;
    request.fields['last_name'] = lastname;
    request.fields['is_staff'] = isAdmin.toString();

    print(request);

    if (image != null) {
      request.files.add(
        await http.MultipartFile.fromPath('picture', image.path),
      );
    }

    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);

    var code = response.statusCode;
    if (code == 200 || code == 201) {
      final data = jsonDecode(response.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', data['token']);
      print(data['is_staff']);
      await prefs.setBool('is_staff', data['is_staff']);
      await prefs.setString('username', data['username']);
    }

    return response;
  }

  static Future<String?> getUsername() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('username');
  }

  static Future<bool> isAdmin() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('is_staff') ?? false;
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('token');
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }
}
