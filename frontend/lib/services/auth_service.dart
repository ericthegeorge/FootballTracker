import 'dart:convert';
// import 'dart:developer';
import 'package:http/http.dart' as http;
import 'dart:io';

class AuthService {
  static const String baseUrl = 'http://127.0.0.1:8000/api'; // testing url

  static Future<http.Response> login(String username, String password) {
    return http.post(
      Uri.parse('$baseUrl/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
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
    return response;
  }
}
