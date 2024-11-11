#include <iostream>
#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;

int main(int argc, char* argv[]) {
    // 检查参数是否足够
    if (argc < 2) {
        std::cerr << "Usage: generate_index <output_dir>" << std::endl;
        return 1;
    }
    std::cout << argv[1] << "debug" << std::endl;


    std::string output_dir = argv[1];

    if (fs::exists(output_dir) && !fs::is_directory(output_dir)) {
        std::cerr << "Error: Specified path is not a directory: " << output_dir << std::endl;
        return 1;
    }
    fs::create_directories(output_dir);

    // 生成 index.html 文件的路径
    std::string index_path = output_dir + "/index.html";

    // 创建并写入 index.html 文件内容
    std::ofstream out(index_path);
    if (!out) {
        std::cerr << "Error: Could not create index.html at " << index_path << std::endl;
        return 1;
    }

    // 写入 HTML 内容
    out << "<!DOCTYPE html>\n";
    out << "<html lang=\"en\">\n";
    out << "<head>\n";
    out << "    <meta charset=\"UTF-8\">\n";
    out << "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
    out << "    <title>Data Processing Result</title>\n";
    out << "    <style>body { font-family: Arial, sans-serif; }</style>\n";
    out << "</head>\n";
    out << "<body>\n";
    out << "    <h1>Data Processing Result</h1>\n";
    out << "    <p>This is the result of processing your uploaded data.</p>\n";
    out << "    <p>Timestamp: " << std::time(nullptr) << "</p>\n";  // 添加时间戳
    out << "    <p>Thank you for using our service!</p>\n";
    out << "</body>\n";
    out << "</html>\n";

    // 关闭文件
    out.close();

    std::cout << "index.html has been generated at " << index_path << std::endl;
    return 0;
}

