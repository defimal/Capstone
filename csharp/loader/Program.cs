using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.IO;
using System.Text.Json;
using System.Xml.Linq;
using MySqlConnector;




class Program
{
    static void Main()
    {
        string basePath = Path.Combine("..", "..", "..", "..", "..", "data", "processed");
        string csvPath = Path.Combine(basePath, "output.csv");
        string jsonPath = Path.Combine(basePath, "output.json");
        string xmlPath = Path.Combine(basePath, "output.xml");
        string dbPath = Path.Combine(basePath, "projects.db");

        string fullCsvPath = Path.GetFullPath(csvPath);
        string fullJsonPath = Path.GetFullPath(jsonPath);
        string fullXmlPath = Path.GetFullPath(xmlPath);
        string fullDbPath = Path.GetFullPath(dbPath);

        Console.WriteLine("Reading CSV from: " + fullCsvPath);

        if (!File.Exists(fullCsvPath))
        {
            Console.WriteLine("ERROR: CSV file not found.");
            return;
        }

        var records = ParseCsvToDictList(fullCsvPath);
        WriteJson(records, fullJsonPath);
        WriteXml(records, fullXmlPath);
        InsertIntoDatabase(records); 

    }

    static List<Dictionary<string, string>> ParseCsvToDictList(string csvFilePath)
    {
        var result = new List<Dictionary<string, string>>();

        using (var reader = new StreamReader(csvFilePath))
        {
            var headerLine = reader.ReadLine();
            var headers = headerLine.Split(',');

            while (!reader.EndOfStream)
            {
                var line = reader.ReadLine();
                var values = line.Split(',');

                var record = new Dictionary<string, string>();
                for (int i = 0; i < headers.Length; i++)
                {
                    record[headers[i].Trim()] = values[i].Trim();
                }

                result.Add(record);
            }
        }

        return result;
    }

    static void WriteJson(List<Dictionary<string, string>> records, string jsonFilePath)
    {
        var json = JsonSerializer.Serialize(records, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(jsonFilePath, json);
        Console.WriteLine("JSON export complete.");
    }

    static void WriteXml(List<Dictionary<string, string>> records, string xmlFilePath)
    {
        var root = new XElement("Projects");

        foreach (var record in records)
        {
            var project = new XElement("Project");
            foreach (var kvp in record)
            {
                project.Add(new XElement(kvp.Key, kvp.Value));
            }
            root.Add(project);
        }

        root.Save(xmlFilePath);
        Console.WriteLine("XML export complete.");
    }

    static void InsertIntoDatabase(List<Dictionary<string, string>> records)
    {
        // ✅ MySQL connection string for localhost (change as needed)
        string connectionString = "server=localhost;user=root;password=YourPassword123!;database=Capstone;";

        using (var conn = new MySqlConnection(connectionString))
        {
            conn.Open();

            var columns = new List<string>(records[0].Keys);

            // ✅ Create table if it doesn't exist
            string createTableSql = "CREATE TABLE IF NOT EXISTS Projects (" +
                                    string.Join(", ", columns.ConvertAll(c => $"`{c}` TEXT")) + ");";

            using (var cmd = new MySqlCommand(createTableSql, conn))
            {
                cmd.ExecuteNonQuery();
            }

            // ✅ Insert data
            foreach (var record in records)
            {
                string insertSql = $"INSERT INTO Projects ({string.Join(",", columns)}) VALUES ({string.Join(",", columns.ConvertAll(c => "@" + c))});";

                using (var cmd = new MySqlCommand(insertSql, conn))
                {
                    foreach (var col in columns)
                    {
                        cmd.Parameters.AddWithValue("@" + col, record[col]);
                    }
                    cmd.ExecuteNonQuery();
                }
            }

            Console.WriteLine("MySQL database export complete.");
        }
    }

}
