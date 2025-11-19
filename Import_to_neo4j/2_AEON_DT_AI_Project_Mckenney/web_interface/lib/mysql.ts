/**
 * MySQL Database Client
 * Singleton pattern for OpenSPG relational data access
 */

import mysql from 'mysql2/promise';

let pool: mysql.Pool | null = null;

export function getMySQLPool(): mysql.Pool {
  if (!pool) {
    const config = {
      host: process.env.MYSQL_HOST || 'openspg-mysql',
      port: parseInt(process.env.MYSQL_PORT || '3306'),
      user: process.env.MYSQL_USER || 'root',
      password: process.env.MYSQL_PASSWORD || 'openspg',
      database: process.env.MYSQL_DATABASE || 'openspg',
      waitForConnections: true,
      connectionLimit: 10,
      queueLimit: 0,
      enableKeepAlive: true,
      keepAliveInitialDelay: 0,
    };

    pool = mysql.createPool(config);
    console.log('✅ MySQL pool initialized:', `${config.host}:${config.port}/${config.database}`);
  }

  return pool;
}

export async function testMySQLConnection(): Promise<boolean> {
  try {
    const pool = getMySQLPool();
    await pool.query('SELECT 1 as test');
    console.log('✅ MySQL connected');
    return true;
  } catch (error) {
    console.error('❌ MySQL connection failed:', error);
    return false;
  }
}

export async function query<T = any>(
  sql: string,
  params?: any[]
): Promise<{ success: boolean; data?: T[]; error?: string }> {
  try {
    const pool = getMySQLPool();
    const [rows] = await pool.query<any[]>(sql, params);
    return {
      success: true,
      data: rows,
    };
  } catch (error) {
    console.error('MySQL query error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

export async function execute(
  sql: string,
  params?: any[]
): Promise<{ success: boolean; affectedRows?: number; insertId?: number; error?: string }> {
  try {
    const pool = getMySQLPool();
    const [result] = await pool.query<mysql.ResultSetHeader>(sql, params);
    return {
      success: true,
      affectedRows: result.affectedRows,
      insertId: result.insertId,
    };
  } catch (error) {
    console.error('MySQL execute error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

export async function getOpenSPGSchema() {
  const sql = `
    SELECT
      TABLE_NAME as tableName,
      TABLE_ROWS as rowCount,
      DATA_LENGTH as dataSize
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = ?
    ORDER BY TABLE_NAME
  `;

  return query(sql, [process.env.MYSQL_DATABASE || 'openspg']);
}

export async function closeMySQLPool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
    console.log('MySQL pool closed');
  }
}

export default {
  getMySQLPool,
  testMySQLConnection,
  query,
  execute,
  getOpenSPGSchema,
  closeMySQLPool,
};
